# Supervisor Meeting Script

## 1. Introduction
This project implements my dissertation proposal for a financial spending analysis and budget prediction system. The aim is to help users upload their transaction records, clean and transform the data, analyse spending behaviour, detect unusual transactions, and predict future expenses.

## 2. Problem motivation
Many users have financial data in spreadsheets but do not have a transparent analytical workflow. My system turns raw spreadsheet data into a structured, explainable, and visual decision-support platform.

## 3. System pipeline
1. Upload CSV or Excel financial data.
2. Run data quality assessment.
3. Clean invalid, duplicate, and incomplete records.
4. Transform the dataset into analysis-ready monthly and categorical structures.
5. Perform descriptive analytics and anomaly detection.
6. Use ARIMA to forecast next-month expenses.
7. Present results through an interactive dashboard and exportable reports.

## 4. Technical justification
- Django provides the secure web framework.
- Pandas and NumPy are used for preprocessing.
- Z-score logic is used for anomaly detection.
- ARIMA is used for time-series forecasting.
- Chart.js is used for visual presentation.

## 5. Demo flow
- Open the dashboard.
- Upload the sample dataset.
- Show the data quality score.
- Explain the cleaning and transformation services.
- Demonstrate filters by date, category, and transaction type.
- Show the actual vs forecast chart.
- Export the PDF report.

## 6. Research contribution
The system is not only a software prototype. It is a complete analytics pipeline that connects data preprocessing, statistical analysis, forecasting, and user-centred dashboard design.

## 7. Future improvements
Future work can include model benchmarking, user-specific recommendations, and more advanced forecasting models.
