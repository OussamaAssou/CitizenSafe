from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Alert, SafetyTip, AbsenceDeclaration, CitizenProfile
from .forms import AlertForm, CitizenProfileForm, AbsenceDeclarationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from police_interface.models import PoliceOfficer, IncidentReport
from postman_interface.models import Postman, Observation
import logging, random

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    try:
        citizen_profile = request.user.citizenprofile
    except CitizenProfile.DoesNotExist:
        # Rediriger vers une page pour créer un profil citoyen ou afficher un message d'erreur
        return redirect('create_citizen_profile')  # ou render une page d'erreur
    
    # Vérifier si le citoyen est actuellement absent
    current_absence = AbsenceDeclaration.objects.filter(
        citizen=request.user,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        is_active=True
    ).first()
    
    is_present = not bool(current_absence)

    user_alerts = Alert.objects.filter(citizen=request.user).order_by('-timestamp')[:5]
    # safety_tips = SafetyTip.objects.all().order_by('-created_at')[:3]
    # Sélectionner aléatoirement un conseil de sécurité
    safety_tips = list(SafetyTip.objects.all())
    if safety_tips:
        random_tips = random.sample(safety_tips, min(3, len(safety_tips)))
    else:
        random_tips = []
    # Récupérer les derniers rapports de police
    police_reports = IncidentReport.objects.filter(concerned_citizen=request.user).order_by('-timestamp')[:5]
    
    # Récupérer les dernières observations des facteurs
    postman_observations = Observation.objects.filter(concerned_citizen=request.user).order_by('-timestamp')[:5]
    context = {
        'is_present': is_present,
        'user_alerts': user_alerts,
        'safety_tips': random_tips,
        'citizen_profile': citizen_profile,
        'police_reports': police_reports,
        'postman_observations': postman_observations,
    }
    return render(request, 'citizen_interface/dashboard.html', context)

@login_required
def create_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.citizen = request.user
            alert.save()
            messages.success(request, 'Alerte créée avec succès.', extra_tags='citizen')
            return redirect('citizen:dashboard')
        else:
            logger.warning(f"Formulaire d'alerte invalide : {form.errors}")
    else:
        form = AlertForm()
    return render(request, 'citizen_interface/create_alert.html', {'form': form})

def create_citizen_profile(request):
    if request.method == 'POST':
        form = CitizenProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = CitizenProfileForm()
    return render(request, 'citizen_interface/create_profile.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CitizenProfileForm(request.POST, instance=request.user.citizenprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.', extra_tags='citizen')
            return redirect('citizen_profile')
    else:
        form = CitizenProfileForm(instance=request.user.citizenprofile)
    return render(request, 'citizen_interface/profile.html', {'form': form})

@login_required
def alert_history(request):
    alerts = Alert.objects.filter(citizen=request.user.citizenprofile).order_by('-timestamp')
    return render(request, 'citizen_interface/alert_history.html', {'alerts': alerts})

@login_required
def declare_absence(request):
    if request.method == 'POST':
        if 'cancel_absence' in request.POST:
            absence_id = request.POST.get('cancel_absence')
            try:
                absence = AbsenceDeclaration.objects.get(id=absence_id, citizen=request.user)
                absence.is_active = False
                absence.save()
                messages.success(request, "L'absence a été annulée avec succès.", extra_tags='citizen')
            except AbsenceDeclaration.DoesNotExist:
                messages.error(request, "L'absence n'a pas pu être annulée.", extra_tags='citizen')
            return redirect('citizen:declare_absence')
        
        form = AbsenceDeclarationForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.citizen = request.user
            absence.save()
            messages.success(request, 'Votre absence a été déclarée avec succès.', extra_tags='citizen')
            return redirect('citizen:dashboard')
    else:
        form = AbsenceDeclarationForm()

    active_absences = AbsenceDeclaration.objects.filter(
        citizen=request.user,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        is_active=True
    ).order_by('end_date')

    past_absences = AbsenceDeclaration.objects.filter(
        citizen=request.user,
        end_date__lt=timezone.now()
    ).order_by('-start_date')[:5]

    context = {
        'form': form,
        'active_absences': active_absences,
        'past_absences': past_absences,
    }
    return render(request, 'citizen_interface/declare_absence.html', context)

@login_required
def view_absences(request):
    absences = AbsenceDeclaration.objects.filter(citizen=request.user.citizenprofile).order_by('-start_date')
    return render(request, 'citizen_interface/view_absences.html', {'absences': absences})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            badge_number = form.cleaned_data.get('badge_number')
            if user_type == 'police':
                PoliceOfficer.objects.create(user=user, badge_number=badge_number)
            elif user_type == 'postman':
                Postman.objects.create(user=user, employee_id=badge_number)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if user.user_type == 'citizen':
                return redirect('citizen:dashboard')
            elif user.user_type == 'police':
                return redirect('police:dashboard')
            elif user.user_type == 'postman':
                return redirect('postman:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'citizen_interface/signup.html', {'form': form})
