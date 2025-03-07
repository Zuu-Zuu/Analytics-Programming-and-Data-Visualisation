import pandas as pd  
import sqlalchemy as db
import yfinance as yf
import json
import requests
import os
import wbgapi as wb

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dagster import asset
from pymongo import MongoClient


@asset
def stock_data_loading() -> dict: 

    tickerStrings = ["PFE", "MRNA","JNJ","BNTX","ABT","TMO","UNH","CVS","AZN"]

    stock_data = yf.download(tickerStrings, group_by='Ticker', period='10y')

    # Transform the DataFrame: stack the ticker symbols to create a multi-index (Date, Ticker), then reset the 'Ticker' level to turn it into a column
    stock_data = stock_data.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)		
    stock_data = stock_data.reset_index().rename(columns={"index":"date"})	

    # Function to get ticker and company name
    def get_ticker_and_name(tickerStrings):
        data = []
        for ticker in tickerStrings:
            stock = yf.Ticker(ticker)
            name = stock.info.get('longName')
            data.append({"Ticker": ticker, "Company Name": name})
        return pd.DataFrame(data)

    # Get the DataFrame
    company_name_df = get_ticker_and_name(tickerStrings)
    stock_data = pd.merge(stock_data, company_name_df, on='Ticker')

    stock_data.to_csv('ticker.csv')
    return {"stock_data": stock_data}


@asset
def who_data_loading() -> dict: 

    base_url = "https://data.who.int/dashboards/covid19/data"
    os.makedirs(os.getcwd(), exist_ok=True)

    response = requests.get(base_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    download_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.csv'):
            full_url = urljoin(base_url, href)
            download_links.append(full_url)

    for file_url in download_links:
        file_name = os.path.basename(file_url)
        file_path = os.path.join(file_name)

        print(f"Downloading {file_url}...")
        file_response = requests.get(file_url)
        file_response.raise_for_status()

        with open(file_path, "wb") as file:
            file.write(file_response.content)
        print(f"Saved to {file_path}")
    print("Download complete.")
    
    covid_who_data = pd.read_csv("WHO-COVID-19-global-daily-data.csv")
    covid_vaccine_who_data = pd.read_csv("vaccination-data.csv")
    return {"covid_who_data": covid_who_data, "covid_vaccine_who_data": covid_vaccine_who_data}


@asset
def wbg_data_loading() -> dict: 
    # GDP_growth
    gdp_data = wb.data.DataFrame('NY.GDP.MKTP.KD.ZG', labels=True) 
    gdp_data = gdp_data.reset_index().rename(columns={"index":"economy"})	
    gdp_data = gdp_data.melt(id_vars=('Country','economy'))
    gdp_data = gdp_data.rename(columns={'variable': 'Year'})
    gdp_data = gdp_data.rename(columns={'value': 'GDP'})
    gdp_data.to_csv('Impact_gdb_data.csv')

    # Unemployment, total (% of total labor force)
    unemployment = wb.data.DataFrame('SL.UEM.TOTL.ZS', labels=True) 
    unemployment = unemployment.reset_index().rename(columns={"index":"economy"})	
    unemployment = unemployment.melt(id_vars=('Country','economy'))
    unemployment = unemployment.rename(columns={'variable': 'Year'})
    unemployment = unemployment.rename(columns={'value': 'Unemployment_Percentage'})
    unemployment.to_csv('Impact_Unemployment.csv')

    # Central government debt, total (% of GDP)
    central_government_debt = wb.data.DataFrame('GC.DOD.TOTL.GD.ZS', labels=True) 
    central_government_debt = central_government_debt.reset_index().rename(columns={"index":"economy"})	
    central_government_debt = central_government_debt.melt(id_vars=('Country','economy'))
    central_government_debt = central_government_debt.rename(columns={'variable': 'Year'})
    central_government_debt = central_government_debt.rename(columns={'value': 'central_government_debt'})
    central_government_debt.to_csv('Impact_central_government_debt.csv')

    return {"gdp_data": gdp_data, "unemployment": unemployment,
    "central_government_debt": central_government_debt}


@asset
def covid_data_json_loading() -> dict: 

    API_KEY = "a60ce11ace3f42238d4cd82b098810a9"
    BASE_URL = "https://api.covidactnow.org/v2/states.timeseries.json"

    def fetch_json_data(api_key):
        try:
            response = requests.get(f"{BASE_URL}?apiKey={api_key}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
            
    json_data = fetch_json_data(API_KEY)

    all_states_data = []
    for state_data in json_data:
        state_name = state_data['state']
        daily_metrics = state_data['actualsTimeseries']
    
        state_df = pd.DataFrame(daily_metrics)
        state_df['date'] = pd.to_datetime(state_df['date'])  
        state_df['state'] = state_name  
        all_states_data.append(state_df)
    df = pd.concat(all_states_data, ignore_index=True)

    covid_data = df[['date','cases', 'deaths','state']]

    return {"covid_data": covid_data}

@asset
def store_in_mongo(covid_data_json_loading: dict) -> None:
 
    mongo_uri = "mongodb://localhost:27017"
    client = MongoClient(mongo_uri)
    mongo_db = client["Analytics_Programming_Project"]
    mongo_collection = mongo_db["Covid_Data"]

    covid_data = covid_data_json_loading['covid_data']
    covid_data = covid_data.to_dict(orient='records')
 
    mongo_collection.delete_many({})
    mongo_collection.insert_many(covid_data)


@asset(deps=[store_in_mongo])
def save_into_postgres(stock_data_loading: dict, who_data_loading: dict, wbg_data_loading: dict) -> None:


    engine = db.create_engine('postgresql://postgres:12321@localhost:5432/Analytics_Programming_Project')

    stock_data = stock_data_loading["stock_data"]
    stock_data.to_sql('stock_data', engine, if_exists='replace', index=False)

    covid_who_data = who_data_loading["covid_who_data"]
    covid_who_data.to_sql('covid_who_data', engine, if_exists='replace', index=False)

    covid_vaccine_who_data = who_data_loading["covid_vaccine_who_data"]
    covid_vaccine_who_data.to_sql('covid_vaccine_who_data', engine, if_exists='replace', index=False)

    #Impact 
    gdp_data = wbg_data_loading["gdp_data"]
    gdp_data.to_sql('gdp_data', engine, if_exists='replace', index=False)

    unemployment = wbg_data_loading["unemployment"]
    unemployment.to_sql('unemployment', engine, if_exists='replace', index=False)

    central_government_debt = wbg_data_loading["central_government_debt"]
    central_government_debt.to_sql('central_government_debt', engine, if_exists='replace', index=False)

    mongo_uri = "mongodb://localhost:27017"
    client = MongoClient(mongo_uri)
    mongo_db = client["Analytics_Programming_Project"]
    mongo_collection = mongo_db["Covid_Data"]

    covid_data = list(mongo_collection.find({}, {"_id": 0}))  # Exclude the MongoDB-generated _id field

    covid_data = pd.DataFrame(covid_data)
    covid_data.to_sql('covid_data', engine, if_exists='replace', index=False)



