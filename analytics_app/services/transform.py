from __future__ import annotations
import pandas as pd

CATEGORY_MAP = {
    'tesco': 'Groceries', 'aldi': 'Groceries', 'asda': 'Groceries',
    'uber': 'Transport', 'train': 'Transport', 'bus': 'Transport',
    'rent': 'Housing', 'salary': 'Income', 'electricity': 'Utilities',
    'gas': 'Utilities', 'netflix': 'Entertainment', 'cinema': 'Entertainment'
}

def normalize_type(value: str) -> str:
    v = str(value).strip().lower()
    return 'Income' if v in ['income','credit','in'] else 'Expense'

def map_category(description: str, category: str) -> str:
    raw = f"{description} {category}".lower()
    for k, mapped in CATEGORY_MAP.items():
        if k in raw:
            return mapped
    category = str(category).strip()
    return category if category else 'Uncategorized'

def transform_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['transaction_type'] = df['type'].apply(normalize_type)
    df['category'] = df.apply(lambda r: map_category(r['description'], r['category']), axis=1)
    df['month'] = df['date'].dt.to_period('M').astype(str)
    return df[['date','month','description','category','amount','transaction_type']]

def monthly_expense_series(df: pd.DataFrame) -> pd.Series:
    expenses = df[df['transaction_type'] == 'Expense'].copy()
    if expenses.empty:
        return pd.Series(dtype='float64')
    monthly = expenses.groupby('month')['amount'].sum().sort_index()
    monthly.index = pd.PeriodIndex(monthly.index, freq='M').to_timestamp()
    return monthly
