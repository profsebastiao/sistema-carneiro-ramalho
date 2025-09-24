from django.urls import path
from . import views

app_name = 'candidates'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/', views.job_search, name='job_search'),
]