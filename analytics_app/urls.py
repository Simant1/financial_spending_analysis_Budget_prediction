from django.urls import path
from .views import (
    dashboard_view,
    upload_dataset_view,
    dataset_detail_view,
    export_cleaned_csv,
    export_summary_pdf,
    architecture_view,
    meeting_script_view,
)

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('upload/', upload_dataset_view, name='upload_dataset'),
    path('dataset/<int:dataset_id>/', dataset_detail_view, name='dataset_detail'),
    path('dataset/<int:dataset_id>/export/csv/', export_cleaned_csv, name='export_cleaned_csv'),
    path('dataset/<int:dataset_id>/export/pdf/', export_summary_pdf, name='export_summary_pdf'),
    path('architecture/', architecture_view, name='architecture_view'),
    path('meeting-script/', meeting_script_view, name='meeting_script_view'),
]
