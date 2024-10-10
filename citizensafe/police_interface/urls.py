from django.urls import path
from . import views

app_name = 'police'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('toggle-duty/', views.toggle_duty_status, name='toggle_duty'),
    path('patrol-optimization/', views.patrol_optimization, name='patrol_optimization'),
    path('create-incident-report/', views.create_incident_report, name='create_incident_report'),
    path('view-alerts/', views.view_alerts, name='view_alerts'),
    path('dashboard/', views.dashboard, name='dashboard'),
]