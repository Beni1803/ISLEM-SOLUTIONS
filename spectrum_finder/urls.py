from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('find-band-block/', views.find_band_block, name='find_band_block'),
]