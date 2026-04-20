# Financial Spending Analysis and Budget Prediction System - Dissertation Plus Edition

<<<<<<< HEAD
The system integrates data analytics techniques with a practical software solution, combining Python-based data processing, time-series forecasting using ARIMA models, and a Django-based web application. The proposed system is intended for personal users and SMEs, providing category-wise expense analysis, detection of overspending behavior, I and short-term budget forecasts.
=======
This project describes the development and design of a web-based system that enables individuals and SMEs to manage their finances by providing them with an analysis of their financial spending, along with budget forecasting capabilities. This project’s primary goal is to design and create a web-based financial management system designed to assist individuals and small/medium-sized businesses (SME) in managing their financial activities by providing them with an effective way to track, analyse and forecast their finances. This platform will support the upload of financial data in common file formats including CSV and Excel so users can access and integrate their existing financial records. Once the user’s financial data is uploaded to the platform, the financial management system will perform sophisticated analysis on that data which will enable users to classify their expenditures, analyse patterns of expenditure, and identify where companies are spending more than necessary or spending inequitably. A key part of this analysis is to identify, flag and make the user aware of potentially fraudulent or excessively large transactions which can alert them to potential financial risks or irregularity. This analysis will be displayed to the user via interactive dashboards and data visuals that provide an easy way for users to comprehend financial data and make informed decisions based on that data. The interactive dashboards will include various types of charts, trend analysis graphs, and aggregated summary statistics to give users a complete view of the company’s overall financial health and performance over time. Additionally, the financial management system will use Advanced Forecasting Techniques such as the ARIMA model as well as using historical financial data and forecasting accurate future expenditure patterns based on that data.
>>>>>>> 9cb425a3b771d39d4c5c0fc595772aed88c34bfd

## New improvements in this edition
- Professional dashboard styling
- Date, category, and transaction-type filters
- Forecast versus actual comparison chart
- Architecture diagram page
<<<<<<< HEAD
-
=======
>>>>>>> 9cb425a3b771d39d4c5c0fc595772aed88c34bfd
- Data quality assessment module
- Automated insights module
- CSV and PDF export

## Core modules
1. Authentication
2. Dataset Upload
3. Data Quality Assessment
4. Data Cleaning
5. Data Transformation
6. Descriptive Analytics
7. Anomaly Detection
8. Forecasting
9. Decision Support Insights
10. Reporting
11. Interactive Dashboard
12. Architecture and Meeting Support

## Required input columns
- date
- description
- category
- amount
- type

## Run
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## What to show in the meeting
- Upload flow
- Quality score
- Cleaning and transformation pipeline
- KPI dashboard
- Filters
- Actual vs forecast comparison
- Anomaly table
- PDF export
- Architecture diagram
<<<<<<< HEAD
-
=======
>>>>>>> 9cb425a3b771d39d4c5c0fc595772aed88c34bfd
