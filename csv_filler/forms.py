from django import forms
from .models import UploadedCSV

class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = UploadedCSV
        fields = ['name', 'csv_file']

class UpdateCSVForm(forms.Form):
    column_name = forms.CharField(label='Column Name')
    row_value = forms.CharField(label='Row Value')
    new_value = forms.CharField(label='New Value to Insert')