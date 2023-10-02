from django.shortcuts import render, redirect
from django.contrib import messages
import csv

# Function to convert CSV to dictionary grouped by Frequency Band
def csv_to_dict(file_path):
    with open(file_path, 'r') as file:
        reader = list(csv.reader(file))
        
        bands_by_frequency = {}
        headers = [row[0] for row in reader]
        
        for col_num in range(1, len(reader[0])):
            freq_band = reader[0][col_num]
            
            if freq_band not in bands_by_frequency:
                bands_by_frequency[freq_band] = []
            
            band = {}
            for row_num, header in enumerate(headers):
                key_name = header.replace("-", "_").replace(" ", "_")  # Replacing hyphens and spaces with underscores
                band[key_name] = reader[row_num][col_num]
            
            bands_by_frequency[freq_band].append(band)

    return bands_by_frequency

# Home view
def home(request):
    band_data_grouped = csv_to_dict('spectrum_finder\static\data\Spectrum Plan.csv')
    selected_band_blocks_grouped = {}

    if request.method == 'POST':
        start_ul = request.POST.get('start_ul')
        stop_ul = request.POST.get('stop_ul')
        
        try:
            start_ul = float(start_ul.strip())
            stop_ul = float(stop_ul.strip())

            # Find matching band-blocks based on the input frequencies
            for freq_band, bands in band_data_grouped.items():
                for band in bands:
                    try:
                        # If Start_(UL) and Stop_(UL) are empty, use Start_(DL) and Stop_(DL) instead
                        start_band_key = "Start_(UL)" if band["Start_(UL)"] else "Start_(DL)"
                        stop_band_key = "Stop_(UL)" if band["Stop_(UL)"] else "Stop_(DL)"

                        start_band = float(band[start_band_key])
                        stop_band = float(band[stop_band_key])

                        if start_band <= start_ul and stop_band >= stop_ul:
                            if freq_band not in selected_band_blocks_grouped:
                                selected_band_blocks_grouped[freq_band] = []
                            selected_band_blocks_grouped[freq_band].append(band)
                    except ValueError:
                        messages.error(request, f'Failed to convert band values: {start_band_key}={band[start_band_key]}, {stop_band_key}={band[stop_band_key]}')

            else:
                count = sum(len(bands) for bands in selected_band_blocks_grouped.values())
                messages.success(request, f'Found {count} band-blocks for the provided frequencies.')

        except ValueError:
            messages.error(request, f'Failed to convert values: start_ul={start_ul}, stop_ul={stop_ul}')
            messages.error(request, 'Please provide valid numbers for the start and stop frequencies.')
    return render(request, 'spectrum_finder/home.html', {
        'selected_band_blocks_grouped': selected_band_blocks_grouped
    })
