from django.urls import path
from . import views

urlpatterns = [
    path('csv_main_page/', views.csv_main_page, name='csv_main_page'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('update/', views.update_csv, name='update_csv'),
    path('csv_main_page/', views.csv_main_page, name='csv_main_page'),
]