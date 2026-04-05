from __future__ import annotations
import math
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def forecast_next_month(monthly_series: pd.Series) -> dict:
    if monthly_series.empty:
        return {'forecast': None, 'mae': None, 'rmse': None, 'message': 'No expense data available.'}
    if len(monthly_series) < 4:
        avg = float(monthly_series.mean())
        return {'forecast': round(avg,2), 'mae': None, 'rmse': None, 'message': 'Average fallback used because series is too short for ARIMA.'}
    train = monthly_series.iloc[:-1]
    test = monthly_series.iloc[-1:]
    try:
        fitted = ARIMA(train, order=(1,1,1)).fit()
        pred = float(fitted.forecast(steps=1).iloc[0])
        actual = float(test.iloc[0])
        mae = abs(actual-pred)
        rmse = math.sqrt((actual-pred)**2)
        full = ARIMA(monthly_series, order=(1,1,1)).fit()
        next_fc = float(full.forecast(steps=1).iloc[0])
        return {'forecast': round(next_fc,2), 'mae': round(mae,2), 'rmse': round(rmse,2), 'message': 'ARIMA forecast generated successfully.'}
    except Exception as exc:
        avg = float(monthly_series.mean())
        return {'forecast': round(avg,2), 'mae': None, 'rmse': None, 'message': f'ARIMA fallback applied: {exc}'}


def build_forecast_comparison(monthly_series: pd.Series) -> dict:
    if monthly_series.empty:
        return {'labels': [], 'actuals': [], 'predictions': [], 'coverage_note': 'No monthly expense history available.'}

    labels = [idx.strftime('%Y-%m') for idx in monthly_series.index]
    actuals = [round(float(v), 2) for v in monthly_series.values]

    if len(monthly_series) < 5:
        avg = float(monthly_series.mean()) if len(monthly_series) else 0.0
        predictions = [round(avg, 2) for _ in monthly_series.values]
        return {
            'labels': labels,
            'actuals': actuals,
            'predictions': predictions,
            'coverage_note': 'Rolling forecast uses average fallback because the series is short.'
        }

    predictions = []
    for i in range(len(monthly_series)):
        if i < 3:
            predictions.append(None)
            continue
        history = monthly_series.iloc[:i]
        try:
            if len(history) < 4:
                predictions.append(round(float(history.mean()), 2))
            else:
                model = ARIMA(history, order=(1,1,1)).fit()
                predictions.append(round(float(model.forecast(steps=1).iloc[0]), 2))
        except Exception:
            predictions.append(round(float(history.mean()), 2))

    return {
        'labels': labels,
        'actuals': actuals,
        'predictions': predictions,
        'coverage_note': 'Forecast comparison shows actual expenses versus rolling one-step-ahead predictions.'
    }
