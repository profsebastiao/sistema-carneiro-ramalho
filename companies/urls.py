from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pipeline/', views.pipeline, name='pipeline'),
]