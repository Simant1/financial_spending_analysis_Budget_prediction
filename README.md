# Financial Spending Analysis and Budget Prediction System - Dissertation Plus Edition

This is an upgraded, more advanced Django implementation of your dissertation proposal. It is designed to look stronger in a supervisor meeting and to demonstrate more technical depth than a basic prototype.

## New improvements in this edition
- Professional dashboard styling
- Date, category, and transaction-type filters
- Forecast versus actual comparison chart
- Architecture diagram page
- Supervisor meeting script page
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
- Meeting script
