from django.shortcuts import render

def home(request):
    return render(request, 'spectrum_finder/home.html')
