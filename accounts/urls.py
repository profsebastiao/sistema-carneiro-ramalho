from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/candidate/', views.register_candidate, name='register_candidate'),
    path('register/company/', views.register_company, name='register_company'),
]