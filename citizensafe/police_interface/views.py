from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Patrol, IncidentReport, PoliceOfficer
from .forms import PatrolForm, IncidentReportForm
from citizen_interface.models import Alert, AbsenceDeclaration, CitizenProfile
import random  # Pour la simulation de l'optimisation des patrouilles
import pickle
import pandas as pd
import numpy as np

User = get_user_model()

# Chargez le modèle
with open('police_interface/ml_models/random_forest_model.pkl', 'rb') as file:
    rf_model = pickle.load(file)

# Fonction pour prédire les zones les plus exposées
def predict_top_zones(hour, minute, top_n=5):
    time_minutes = hour * 60 + minute
    
    # Obtenir les probabilités pour chaque zone
    probabilities = rf_model.predict_proba([[time_minutes]])[0]

    # Créer un dictionnaire de correspondance entre les indices et les noms de zones
    zone_names = dict(IncidentReport.AREA_CHOICES)
    
    # Trier les zones par probabilité décroissante
    sorted_indices = np.argsort(probabilities)[::-1]
    
    # Sélectionner les top_n zones
    top_zones = [zone_names[str(int(zone))] for zone in rf_model.classes_[sorted_indices[:top_n]]]
    top_probs = probabilities[sorted_indices[:top_n]]
    
    return list(zip(top_zones, top_probs))

@login_required
def dashboard(request):
    try:
        officer = PoliceOfficer.objects.get(user=request.user)
        active_alerts = Alert.objects.filter(is_active=True).select_related('citizen').order_by('-timestamp')[:5]
        recent_incidents = IncidentReport.objects.order_by('-timestamp')[:5]
        
        context = {
            'officer': officer,
            'active_alerts': active_alerts,
            'recent_incidents': recent_incidents,
        }
        return render(request, 'police_interface/dashboard.html', context)
    except PoliceOfficer.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme officier de police.")
        return redirect('home')  # Ou une autre page appropriée

@login_required
def toggle_duty_status(request):
    try:
        officer = PoliceOfficer.objects.get(user=request.user)
        officer.is_on_duty = not officer.is_on_duty
        officer.save()
        status = "en service" if officer.is_on_duty else "hors service"
        messages.success(request, f"Vous êtes maintenant {status}.")
    except PoliceOfficer.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme officier de police.")
    return redirect('police:dashboard')

@login_required
def patrol_optimization(request):
    try:
        officer = PoliceOfficer.objects.get(user=request.user)
        if not officer.is_on_duty:
            return render(request, 'police_interface/not_on_duty.html')
    except PoliceOfficer.DoesNotExist:
        return render(request, 'police_interface/not_police_officer.html')

    if request.method == 'POST':
        hour = int(request.POST.get('hour', 0))
        minute = int(request.POST.get('minute', 0))
        top_n = int(request.POST.get('top_n', 5))
    else:
        current_time = timezone.now()
        hour = current_time.hour
        minute = current_time.minute
        top_n = 5

    # Prédire les zones à risque
    top_zones = predict_top_zones(hour, minute, top_n)

    # Récupérer les absences actives
    current_time = timezone.now()
    active_absences = AbsenceDeclaration.objects.filter(
        is_active=True,
        start_date__lte=current_time,
        end_date__gte=current_time
    )

    officers = PoliceOfficer.objects.filter(is_on_duty=True)
    optimized_patrols = []
    
    for officer in officers:
        if active_absences:
            absence = active_absences.first()
            assigned_location = f"Domicile de {absence.citizen.first_name} {absence.citizen.last_name}"
            active_absences = active_absences.exclude(id=absence.id)
        else:
            if top_zones:
                assigned_zone, probability = top_zones.pop(0)
                assigned_location = f"{assigned_zone} (Probabilité: {probability:.2f})"
            else:
                assigned_location = "Zone aléatoire"
        
        optimized_patrols.append({
            'officer': officer,
            'location': assigned_location
        })
    
    context = {
        'optimized_patrols': optimized_patrols,
        'current_time': f"{hour:02d}:{minute:02d}",
        'remaining_top_zones': top_zones,
        'hour': hour,
        'minute': minute,
        'top_n': top_n
    }
    return render(request, 'police_interface/patrol_optimization.html', context)

@login_required
def create_incident_report(request):
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporting_officer = request.user.policeofficer
            
            concerned_citizen = form.cleaned_data.get('concerned_citizen')
            if concerned_citizen:
                report.concerned_citizen = concerned_citizen
            
            report.save()
            messages.success(request, 'Rapport d\'incident créé avec succès.')
            return redirect('police:dashboard')
    else:
        form = IncidentReportForm()
    
    return render(request, 'police_interface/create_incident_report.html', {'form': form})

@login_required
def view_alerts(request):
    alerts = Alert.objects.filter(is_active=True).order_by('-timestamp')
    return render(request, 'police_interface/view_alerts.html', {'alerts': alerts})