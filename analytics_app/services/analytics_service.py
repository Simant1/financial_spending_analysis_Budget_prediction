from __future__ import annotations
import math
import pandas as pd


def detect_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    expenses = df[df['transaction_type'] == 'Expense'].copy()
    if expenses.empty:
        return expenses.iloc[0:0]
    mean_val = expenses['amount'].mean()
    std_val = expenses['amount'].std(ddof=0)
    if std_val == 0 or math.isnan(std_val):
        expenses['z_score'] = 0
        expenses['is_anomaly'] = False
        return expenses[expenses['is_anomaly']]
    expenses['z_score'] = (expenses['amount'] - mean_val) / std_val
    expenses['is_anomaly'] = expenses['z_score'].abs() >= threshold
    return expenses[expenses['is_anomaly']].sort_values('amount', ascending=False)


def compute_summary(df: pd.DataFrame) -> dict:
    income_total = float(df.loc[df['transaction_type']=='Income','amount'].sum())
    expense_total = float(df.loc[df['transaction_type']=='Expense','amount'].sum())
    balance = income_total - expense_total
    expenses_only = df[df['transaction_type']=='Expense'].copy()
    category_summary = (expenses_only.groupby('category', as_index=False)['amount'].sum().sort_values('amount', ascending=False))
    monthly_trend = (expenses_only.groupby('month', as_index=False)['amount'].sum().sort_values('month'))
    anomalies = detect_anomalies(df)
    top_category = category_summary.iloc[0]['category'] if not category_summary.empty else 'N/A'
    avg_expense = float(expenses_only['amount'].mean()) if not expenses_only.empty else 0.0
    savings_rate = ((balance / income_total) * 100) if income_total else 0.0
    return {
        'income_total': round(income_total,2),
        'expense_total': round(expense_total,2),
        'balance': round(balance,2),
        'avg_expense': round(avg_expense,2),
        'top_category': top_category,
        'transaction_count': int(len(df)),
        'anomaly_count': int(len(anomalies)),
        'savings_rate': round(savings_rate,2),
        'category_summary': category_summary.to_dict(orient='records'),
        'monthly_trend': monthly_trend.to_dict(orient='records'),
        'anomalies': anomalies.to_dict(orient='records'),
        'recent_transactions': df.sort_values('date', ascending=False).head(12).to_dict(orient='records'),
    }
