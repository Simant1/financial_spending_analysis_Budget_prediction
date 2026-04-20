# Financial Spending Analysis and Budget Prediction System - Dissertation Plus Edition

The system integrates data analytics techniques with a practical software solution, combining Python-based data processing, time-series forecasting using ARIMA models, and a Django-based web application. The proposed system is intended for personal users and SMEs, providing category-wise expense analysis, detection of overspending behavior, I and short-term budget forecasts.

## New improvements in this edition
- Professional dashboard styling
- Date, category, and transaction-type filters
- Forecast versus actual comparison chart
- Architecture diagram page
-
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
-
