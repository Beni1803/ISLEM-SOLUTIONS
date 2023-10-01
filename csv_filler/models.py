from django.db import models

class UploadedCSV(models.Model):
    name = models.CharField(max_length=255)
    csv_file = models.FileField(upload_to='uploaded_csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
