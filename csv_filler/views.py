from django.shortcuts import render, redirect
from .models import UploadedCSV
from .forms import UploadCSVForm, UpdateCSVForm
import csv
import io

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('update_csv')
    else:
        form = UploadCSVForm()
    return render(request, 'csv_filler/upload_csv.html', {'form': form})

def update_csv(request):
    if request.method == 'POST':
        form = UpdateCSVForm(request.POST)
        if form.is_valid():
            # Load the latest uploaded CSV
            latest_csv = UploadedCSV.objects.latest('uploaded_at')
            with open(latest_csv.csv_file.path, 'r+', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                # Convert reader to a list for in-memory modification
                rows = list(reader)

                # Modify the CSV data in memory based on the form inputs
                for row in rows:
                    if row[form.cleaned_data['column_name']] == form.cleaned_data['row_value']:
                        row[form.cleaned_data['column_name']] = form.cleaned_data['new_value']
                
                # Write the updated data back to the CSV
                csv_file.seek(0)
                writer = csv.DictWriter(csv_file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
                csv_file.truncate()  # Remove any remaining old data after the new data

            return redirect('update_csv')
    else:
        form = UpdateCSVForm()
    return render(request, 'csv_filler/update_csv.html', {'form': form})
