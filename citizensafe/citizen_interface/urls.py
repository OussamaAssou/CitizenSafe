from django.urls import path
from . import views

app_name = 'citizen'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('create-alert/', views.create_alert, name='create_alert'),
    path('alert-history/', views.alert_history, name='alert_history'),
    path('declare-absence/', views.declare_absence, name='declare_absence'),
    path('view-absences/', views.view_absences, name='view_absences'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-profile/', views.create_citizen_profile, name='create_citizen_profile'),
]