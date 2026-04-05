from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = ['date','description','category','amount','type']

def assess_data_quality(df: pd.DataFrame) -> dict:
    cols = [str(c).strip().lower().replace(' ','_') for c in df.columns]
    df = df.copy()
    df.columns = cols
    present = sum(1 for c in REQUIRED_COLUMNS if c in df.columns)
    structure_score = (present / len(REQUIRED_COLUMNS)) * 100
    if present != len(REQUIRED_COLUMNS):
        return {
            'quality_score': round(structure_score, 2),
            'missing_columns': [c for c in REQUIRED_COLUMNS if c not in df.columns],
            'duplicate_rows': 0,
            'missing_rate': None,
            'row_count': len(df),
            'valid_amount_rate': None,
        }
    missing_rate = df[REQUIRED_COLUMNS].isna().mean().mean() * 100
    duplicate_rows = int(df.duplicated().sum())
    valid_amount_rate = pd.to_numeric(df['amount'], errors='coerce').notna().mean() * 100
    quality_score = max(0.0, structure_score * 0.5 + (100 - missing_rate) * 0.3 + valid_amount_rate * 0.2 - duplicate_rows)
    return {
        'quality_score': round(min(100.0, quality_score), 2),
        'missing_columns': [],
        'duplicate_rows': duplicate_rows,
        'missing_rate': round(float(missing_rate), 2),
        'row_count': len(df),
        'valid_amount_rate': round(float(valid_amount_rate), 2),
    }
