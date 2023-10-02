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
        combined_inputs = request.POST.get('frequency_range').split()
        
        buffer = []

        for part in combined_inputs:
            # If current part contains a dash, it's a range
            if '-' in part:
                buffer.append(part)

                # If there's a `/`, it means we have both UL and DL in the buffer
                if '/' in part:
                    # Split the current part into UL and DL
                    ul_input, dl_input = part.split('/')
                    process_input(ul_input, dl_input, band_data_grouped, selected_band_blocks_grouped)
                    buffer = []  # Clear buffer

                # If buffer has 2 elements without a `/`, it's two DL inputs
                elif len(buffer) == 2:
                    dl_input = buffer[0]
                    process_input(dl_input, None, band_data_grouped, selected_band_blocks_grouped)
                    buffer = [buffer[1]]  # Keep the last element for next iteration

            else:
                messages.error(request, f'Invalid input detected: {part}')

        # Handle any remaining items in the buffer
        if buffer:
            if len(buffer) == 1:
                dl_input = buffer[0]
                process_input(dl_input, None, band_data_grouped, selected_band_blocks_grouped)
            else:
                messages.error(request, f'Unexpected buffer state: {buffer}')
        
        count = sum(len(bands) for bands in selected_band_blocks_grouped.values())
        messages.success(request, f'Found {count} band-blocks for the provided frequencies.')

    return render(request, 'spectrum_finder/home.html', {
        'selected_band_blocks_grouped': selected_band_blocks_grouped
    })

def process_input(ul_input, dl_input, band_data_grouped, selected_band_blocks_grouped):
    try:
        if ul_input:
            start_ul, stop_ul = [float(val) for val in ul_input.split('-')]
        if dl_input:
            start_dl, stop_dl = [float(val) for val in dl_input.split('-')]
        if not ul_input:
            start_ul, stop_ul = start_dl, stop_dl

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
    except ValueError:
        messages.error(request, f'Failed to convert input values: UL={ul_input}, DL={dl_input}')