from __future__ import annotations

def generate_insights(summary: dict, quality: dict, forecast: dict) -> list[str]:
    insights = []
    if summary['expense_total'] > summary['income_total']:
        insights.append('Total expenses are higher than total income, indicating a negative budget position.')
    else:
        insights.append('Income is currently higher than expenses, suggesting a positive overall budget balance.')
    if summary['top_category'] != 'N/A':
        insights.append(f"The highest spending category is {summary['top_category']}, which should be reviewed for optimization.")
    if summary['anomaly_count'] > 0:
        insights.append(f"{summary['anomaly_count']} anomalous transaction(s) were detected using z-score thresholding.")
    if forecast.get('forecast') is not None:
        insights.append(f"The forecasted next-month expense is {forecast['forecast']}, useful for forward budget planning.")
    if quality.get('quality_score') is not None:
        insights.append(f"Dataset quality score is {quality['quality_score']} out of 100 based on completeness, structure, and validity.")
    return insights
