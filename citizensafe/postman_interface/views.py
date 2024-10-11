from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Observation
from .forms import ObservationForm

User = get_user_model()

@login_required
def dashboard(request):
    recent_observations = Observation.objects.filter(postman=request.user.postman).order_by('-timestamp')[:5]
    context = {
        'recent_observations': recent_observations,
    }
    return render(request, 'postman_interface/dashboard.html', context)

@login_required
def create_observation(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.postman = request.user.postman
            
            # Le champ concerned_citizen contient maintenant directement l'objet User
            observation.concerned_citizen = form.cleaned_data['concerned_citizen']
            
            observation.save()
            messages.success(request, 'Observation créée avec succès.', extra_tags='postman')
            return redirect('postman:dashboard')
    else:
        form = ObservationForm()
    
    return render(request, 'postman_interface/create_observation.html', {'form': form})

@login_required
def view_route(request):
    # Ici, vous pouvez implémenter la logique pour afficher la route du facteur
    # Pour le prototype, nous utiliserons une route fictive
    route = [
        {'address': '123 Rue Principale', 'time': '09:00'},
        {'address': '456 Avenue Centrale', 'time': '09:30'},
        {'address': '789 Boulevard du Parc', 'time': '10:00'},
    ]
    return render(request, 'postman_interface/view_route.html', {'route': route})

@login_required
def observation_history(request):
    observations = Observation.objects.filter(postman=request.user.postman).order_by('-timestamp')
    return render(request, 'postman_interface/observation_history.html', {'observations': observations})