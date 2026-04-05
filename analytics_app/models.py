from django.db import models
from django.contrib.auth.models import User

class UploadedDataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rows_processed = models.PositiveIntegerField(default=0)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    dataset = models.ForeignKey(UploadedDataset, related_name='transactions', on_delete=models.CASCADE)
    date = models.DateField()
    month = models.CharField(max_length=7)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20)
    is_anomaly = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
