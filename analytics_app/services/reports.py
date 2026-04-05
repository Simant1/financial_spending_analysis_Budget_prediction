from __future__ import annotations
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')

def build_summary_pdf(dataset_name: str, summary: dict, forecast: dict, quality: dict, insights: list[str]) -> bytes:
    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 50
    pdf.setFont('Helvetica-Bold', 18)
    pdf.drawString(40, y, 'Financial Spending Analysis Report')
    y -= 26
    pdf.setFont('Helvetica', 11)
    lines = [
        f'Dataset: {dataset_name}',
        f'Quality Score: {quality.get("quality_score")}',
        f'Total Income: {summary.get("income_total")}',
        f'Total Expense: {summary.get("expense_total")}',
        f'Net Balance: {summary.get("balance")}',
        f'Top Category: {summary.get("top_category")}',
        f'Anomaly Count: {summary.get("anomaly_count")}',
        f'Next Month Forecast: {forecast.get("forecast")}',
        f'Forecast Note: {forecast.get("message")}',
        '', 'Key Insights:'
    ]
    for item in insights:
        lines.append(f'- {item}')
    for line in lines:
        pdf.drawString(40, y, str(line)[:110])
        y -= 18
        if y < 70:
            pdf.showPage(); y = height - 50; pdf.setFont('Helvetica', 11)
    pdf.save()
    return buf.getvalue()
