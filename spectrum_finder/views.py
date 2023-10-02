from django.shortcuts import render

def home(request):
    return render(request, 'spectrum_finder/home.html')

def find_band_block(request):
    form = FrequencyRangeForm(request.POST or None)
    band_block = None

    if form.is_valid():
        csv_file = 'spectrum_finder\static\data\Spectrum Plan.csv'
        df = pd.read_csv(csv_file)

        # Extract start and stop frequencies from form
        start_ul = form.cleaned_data['start_ul']
        stop_ul = form.cleaned_data['stop_ul']

        # Calculate the center frequency from the provided range
        center_ul = (start_ul + stop_ul) / 2

        # Allow for a small deviation, say +/- 0.5 MHz
        deviation = 0.5

        # Find the corresponding band-block using the center frequency
        match = df[
            (df['Centre (UL)'] >= center_ul - deviation) &
            (df['Centre (UL)'] <= center_ul + deviation)
        ]

        if not match.empty:
            band_block = match['Band-Block'].values[0]

    return render(request, 'find_band_block.html', {'form': form, 'band_block': band_block})

