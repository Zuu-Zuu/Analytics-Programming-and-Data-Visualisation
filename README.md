# Data Analytics of COVID-19's Global Impact

## Overview
This project, **Data Analytics of COVID-19's Global Impact**, explores the social and economic effects of the COVID-19 pandemic. It focuses on **COVID-19 cases, vaccinations, economic indicators, and stock market trends** to understand their impact on global GDP, unemployment, and government debts. The project leverages **data analytics, visualization, and machine learning** to extract meaningful insights.

## Project Structure
- **AnalyticProgramming_Project_Dagster/** → Workflow orchestration scripts using Dagster.
- **Project Report/** → Research documentation and key findings.
- **Tableau_Dashboard/** → Interactive visualization dashboards.
- **Visualization_with_Python/** → Python scripts for data analysis & visualization.

## Datasets Used
### COVID-19 Data
1. **COVID Cases & Deaths Data** → Daily infections, deaths, and regional demographics.
2. **COVID Vaccine Data** → Vaccine rollout progress by country.
3. **COVID Vaccine Metadata** → Details about vaccine manufacturers and availability.

### Economic Data
4. **GDP Data** → Economic trends across different nations.
5. **Unemployment Data** → Unemployment spikes during the pandemic.
6. **Government Debt Data** → Changes in national debt due to pandemic relief measures.

### Stock Market Data
7. **Stock Market Data** → Performance of industries affected by COVID-19 (e.g., pharmaceuticals, airlines, tech).

## Technologies Used
- **Programming:** Python, SQL
- **Data Processing:** Pandas, NumPy, ETL Pipelines
- **Data Storage:** PostgreSQL, MongoDB
- **Visualization:** Tableau, Matplotlib, Seaborn, Plotly
- **Machine Learning:** Time-series forecasting, trend analysis
- **Orchestration:** Dagster for workflow automation

## How to Run the Project
### 1 Clone the Repository
```bash
git clone https://github.com/Zuu-Zuu/Analytics-Programming-and-Data-Visualisation.git
cd Analytics-Programming-and-Data-Visualisation
```

### 2 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3 Run Data Processing
```bash
python data_processing.py
```

### 4 Start the Visualization Dashboard (Tableau)
- Open `Tableau_Dashboard/TableauWorkbook.twbx`

### 5 Run ETL Pipeline (Dagster)
```bash
dagster pipeline execute -p dagster_pipeline.py
```



