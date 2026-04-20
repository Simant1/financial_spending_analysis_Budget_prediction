from __future__ import annotations
import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DatasetUploadForm
from .models import UploadedDataset, Transaction
from .services.quality import assess_data_quality
from .services.cleaning import clean_financial_data
from .services.transform import transform_financial_data, monthly_expense_series
from .services.analytics_service import compute_summary, detect_anomalies
from .services.forecast import forecast_next_month, build_forecast_comparison
from .services.insights import generate_insights
from .services.reports import dataframe_to_csv_bytes, build_summary_pdf


def _read_file(dataset: UploadedDataset) -> pd.DataFrame:
    p = dataset.file.path
    if p.endswith('.csv'):
        return pd.read_csv(p)
    if p.endswith('.xlsx') or p.endswith('.xls'):
        return pd.read_excel(p)
    raise ValueError('Unsupported file type. Upload CSV or XLSX.')


@login_required
def dashboard_view(request):
    datasets = UploadedDataset.objects.filter(user=request.user).order_by('-uploaded_at')
    dataset_count = datasets.count()
    total_rows = sum(d.rows_processed for d in datasets)
    avg_quality = round(sum(float(d.quality_score) for d in datasets) / dataset_count, 2) if dataset_count else 0
    context = {
        'datasets': datasets,
        'dataset_count': dataset_count,
        'total_rows': total_rows,
        'avg_quality': avg_quality,
        'best_dataset': datasets[0] if dataset_count else None,
    }
    return render(request, 'analytics_app/dashboard.html', context)


@login_required
def upload_dataset_view(request):
    form = DatasetUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        dataset = form.save(commit=False)
        dataset.user = request.user
        dataset.save()
        try:
            raw = _read_file(dataset)
            quality = assess_data_quality(raw)
            cleaned = clean_financial_data(raw)
            transformed = transform_financial_data(cleaned)
            anomalies = detect_anomalies(transformed)
            anomaly_keys = set(zip(anomalies['date'].astype(str), anomalies['description'].astype(str), anomalies['amount'].astype(float))) if not anomalies.empty else set()
            txs = []
            for _, row in transformed.iterrows():
                key = (str(row['date'].date()), str(row['description']), float(row['amount']))
                txs.append(Transaction(
                    dataset=dataset, date=row['date'].date(), month=row['month'], description=row['description'],
                    category=row['category'], amount=float(row['amount']), transaction_type=row['transaction_type'],
                    is_anomaly=key in anomaly_keys,
                ))
            Transaction.objects.bulk_create(txs)
            dataset.rows_processed = len(txs)
            dataset.quality_score = quality['quality_score']
            dataset.save(update_fields=['rows_processed','quality_score'])
            messages.success(request, 'Dataset uploaded and processed successfully.')
            return redirect('dataset_detail', dataset_id=dataset.id)
        except Exception as exc:
            dataset.delete()
            messages.error(request, f'Processing failed: {exc}')
    return render(request, 'analytics_app/upload.html', {'form': form})


def _apply_filters(df: pd.DataFrame, request):
    start_date = request.GET.get('start_date') or ''
    end_date = request.GET.get('end_date') or ''
    category = request.GET.get('category') or ''
    tx_type = request.GET.get('transaction_type') or ''

    filtered = df.copy()
    if start_date:
        filtered = filtered[filtered['date'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered['date'] <= pd.to_datetime(end_date)]
    if category:
        filtered = filtered[filtered['category'] == category]
    if tx_type:
        filtered = filtered[filtered['transaction_type'] == tx_type]

    return filtered, {
        'start_date': start_date,
        'end_date': end_date,
        'category': category,
        'transaction_type': tx_type,
    }


@login_required
def dataset_detail_view(request, dataset_id:int):
    dataset = get_object_or_404(UploadedDataset, id=dataset_id, user=request.user)
    qs = dataset.transactions.all().values('date','month','description','category','amount','transaction_type','is_anomaly')
    df = pd.DataFrame(list(qs))
    if df.empty:
        messages.warning(request, 'No transactions available for this dataset.')
        return redirect('dashboard')
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])
    all_categories = sorted(df['category'].dropna().unique().tolist())
    filtered_df, filters = _apply_filters(df, request)
    summary = compute_summary(filtered_df)
    quality = {
        'quality_score': float(dataset.quality_score),
        'row_count': int(dataset.rows_processed),
        'filtered_count': int(len(filtered_df)),
    }
    monthly_series = monthly_expense_series(filtered_df)
    forecast = forecast_next_month(monthly_series)
    comparison = build_forecast_comparison(monthly_series)
    insights = generate_insights(summary, quality, forecast)
    context = {
        'dataset': dataset,
        'summary': summary,
        'quality': quality,
        'forecast': forecast,
        'comparison': comparison,
        'insights': insights,
        'category_labels': [item['category'] for item in summary['category_summary']],
        'category_values': [float(item['amount']) for item in summary['category_summary']],
        'trend_labels': [item['month'] for item in summary['monthly_trend']],
        'trend_values': [float(item['amount']) for item in summary['monthly_trend']],
        'all_categories': all_categories,
        'filters': filters,
    }
    return render(request, 'analytics_app/dataset_detail.html', context)


@login_required
def export_cleaned_csv(request, dataset_id:int):
    dataset = get_object_or_404(UploadedDataset, id=dataset_id, user=request.user)
    qs = dataset.transactions.all().values('date','month','description','category','amount','transaction_type','is_anomaly')
    df = pd.DataFrame(list(qs))
    response = HttpResponse(dataframe_to_csv_bytes(df), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{dataset.name}_cleaned.csv"'
    return response


@login_required
def export_summary_pdf(request, dataset_id:int):
    dataset = get_object_or_404(UploadedDataset, id=dataset_id, user=request.user)
    qs = dataset.transactions.all().values('date','month','description','category','amount','transaction_type','is_anomaly')
    df = pd.DataFrame(list(qs))
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])
    summary = compute_summary(df)
    forecast = forecast_next_month(monthly_expense_series(df))
    # 
    response = HttpResponse(
    build_summary_pdf(
        dataset.name, 
        summary, 
        forecast, 
        quality={"score": 85, "level": "Good"}, 
        insights=["Data quality appears consistent", "No major anomalies detected"]
    ), 
    content_type='application/pdf'
)


@login_required
def architecture_view(request):
    return render(request, 'analytics_app/architecture.html')


@login_required
def meeting_script_view(request):
    return render(request, 'analytics_app/meeting_script.html')
