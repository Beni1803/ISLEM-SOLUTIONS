from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('update/', views.update_csv, name='update_csv'),
    path('download_csv/', views.download_csv, name='download_csv'),

]