from django.contrib import admin
from .models import UploadedDataset, Transaction
admin.site.register(UploadedDataset)
admin.site.register(Transaction)
