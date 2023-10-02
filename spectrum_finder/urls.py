from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spectrum_finder/', views.home, name='find_band_blocks'),
]