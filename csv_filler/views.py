from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import UploadedCSV
from .forms import UploadCSVForm, UpdateCSVForm
import csv
import logging

logger = logging.getLogger(__name__)

def validate_csv_consistency(csv_path):
    inconsistent_lines = []
    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        column_count = len(next(reader))  # Get column count from the header row
        for line_number, row in enumerate(reader, start=2):  # Start from 2 because we've already read the header
            if len(row) != column_count:
                inconsistent_lines.append(line_number)
    return inconsistent_lines

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Validate the uploaded CSV for consistency
            latest_csv = UploadedCSV.objects.latest('uploaded_at')
            inconsistent_lines = validate_csv_consistency(latest_csv.csv_file.path)
            if inconsistent_lines:
                # Inform the user about inconsistent lines but continue processing
                lines_str = ", ".join(str(line) for line in inconsistent_lines)
                messages.warning(request, f"Data inconsistency detected on lines: {lines_str}. Proceeding with valid data.")

            return redirect('update_csv')
    else:
        form = UploadCSVForm()
    return render(request, 'csv_filler/upload_csv.html', {'form': form})

def update_csv(request):
    csv.field_size_limit(2147483647)

    if request.method == 'POST':
        form = UpdateCSVForm(request.POST)
        if form.is_valid():
            try:
                latest_csv = UploadedCSV.objects.latest('uploaded_at')
                with open(latest_csv.csv_file.path, 'r+', newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    rows = list(reader)
                    
                    # Determine the title of the first column
                    row_title_column = reader.fieldnames[0]

                    # Gather unique values from the first column for potential row values
                    unique_row_values = set(row[row_title_column] for row in rows)
                    
                    # Extract potential row values from user input by checking against unique_row_values
                    potential_row_values = [val for val in unique_row_values if val in form.cleaned_data['row_value']]
                    
                    # Extract potential column names from user input by checking against all column names
                    potential_column_names = [col for col in reader.fieldnames if col in form.cleaned_data['column_name']]
                    
                    if not potential_column_names:
                        messages.error(request, "No matching column names found in the CSV.")
                        return redirect('update_csv')
                    
                    total_rows = len(rows)
                    rows_updated = 0

                    for row in rows:
                        for column_name in potential_column_names:
                            if row[row_title_column] in potential_row_values:
                                row[column_name] = form.cleaned_data['new_value']
                                rows_updated += 1

                    csv_file.seek(0)
                    writer = csv.DictWriter(csv_file, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                    csv_file.truncate()

                    messages.success(request, 'CSV updated successfully!')
                    messages.info(request, f"Total rows in CSV: {total_rows}")
                    messages.info(request, f"Number of rows updated: {rows_updated}")

                return redirect('update_csv')
            except Exception as e:
                logger.error(f"Error updating CSV: {e}")
                messages.error(request, f"Error updating CSV: {e}")
    else:
        form = UpdateCSVForm()
    return render(request, 'csv_filler/update_csv.html', {'form': form})

def download_csv(request):
    try:
        latest_csv = UploadedCSV.objects.latest('uploaded_at')
        with open(latest_csv.csv_file.path, 'r', newline='') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{latest_csv.csv_file.name}"'
            return response
    except Exception as e:
        logger.error(f"Error downloading CSV: {e}")
        messages.error(request, f"Error downloading CSV: {e}")
        return redirect('upload_csv')
