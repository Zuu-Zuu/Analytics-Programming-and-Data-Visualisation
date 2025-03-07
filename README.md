# Data Analytics of COVID-19's Global Impact

## Overview
This project, **Data Analytics of COVID-19's Global Impact**, explores the social and economic effects of the COVID-19 pandemic. It focuses on **COVID-19 cases, vaccinations, economic indicators, and stock market trends** to understand their impact on global GDP, unemployment, and government debts. The project leverages **data analytics, visualization, and machine learning** to extract meaningful insights.

## Project Structure
- **AnalyticProgramming_Project_Dagster/** → Contains workflow orchestration scripts using Dagster.
- **Project Report/** → Documentation and findings from the research.
- **Tableau_Dashboard/** → Interactive visualization dashboards.
- **Visualization_with_Python/** → Python scripts for data processing & visualization.

## Datasets Used
### COVID-19 Data
1. **COVID Cases & Deaths Data** → Daily cases, deaths, and demographic information.
2. **COVID Vaccine Data** → Vaccine administration, doses, and booster statistics.
3. **COVID Vaccine Metadata** → Manufacturing and country-wise vaccine details.

### Economic Data
4. **GDP Data** → Global economic growth rate over the years.
5. **Unemployment Data** → Global unemployment trends before, during, and after COVID-19.
6. **Central Government Debt Data** → Government debt changes due to pandemic policies.

### Stock Market Data
7. **Stock Market Data** → Performance of pharmaceutical companies like Pfizer, Moderna, and AstraZeneca.

## Technologies Used
- **Programming:** Python, SQL
- **Data Processing:** Pandas, NumPy, ETL Pipelines
- **Data Storage:** PostgreSQL, MongoDB
- **Visualization:** Tableau, Matplotlib, Seaborn
- **Orchestration:** Dagster for workflow automation

### Run ETL Pipeline (Dagster)
```bash
dagster pipeline execute -p dagster_pipeline.py
```

