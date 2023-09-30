from django.shortcuts import render
from .models import WebApp

def dashboard_view(request):
    apps = WebApp.objects.all()
    context = {'apps': apps}
    return render(request, 'dashboard/dashboard.html', context)
