from django.urls import path
from . import views

app_name = 'postman'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-observation/', views.create_observation, name='create_observation'),
    path('view-route/', views.view_route, name='view_route'),
    path('observation-history/', views.observation_history, name='observation_history'),
    path('dashboard/', views.dashboard, name='dashboard'),
]