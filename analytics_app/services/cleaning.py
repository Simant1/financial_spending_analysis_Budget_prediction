from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = ['date','description','category','amount','type']

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).strip().lower().replace(' ','_') for c in df.columns]
    return df

def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df.copy())
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df = df[REQUIRED_COLUMNS].copy()
    df['description'] = df['description'].fillna('No description').astype(str).str.strip()
    df['category'] = df['category'].fillna('Uncategorized').astype(str).str.strip()
    df['type'] = df['type'].fillna('Expense').astype(str).str.strip()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date','amount'])
    df = df.drop_duplicates()
    df['category'] = df['category'].replace({'':'Uncategorized'})
    df['description'] = df['description'].replace({'':'No description'})
    df['amount'] = df['amount'].round(2)
    return df
