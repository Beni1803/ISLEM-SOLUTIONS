from django.contrib import admin
from .models import UploadedCSV

@admin.register(UploadedCSV)
class UploadedCSVAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at')
