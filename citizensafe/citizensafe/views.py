from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from citizen_interface.models import CitizenProfile
from police_interface.models import PoliceOfficer
from postman_interface.models import Postman
from .forms import UserProfileForm, CitizenProfileForm, PoliceOfficerForm, PostmanForm

@login_required
def profile_router(request):
    user = request.user
    if hasattr(user, 'citizenprofile'):
        return redirect('citizen:dashboard')
    elif hasattr(user, 'policeofficer'):
        return redirect('police:dashboard')
    elif hasattr(user, 'postman'):
        return redirect('postman:dashboard')
    else:
        # Gérer le cas où l'utilisateur n'a pas de profil spécifique
        return redirect('home')
    
@login_required
def home_dashboard(request):
    user = request.user
    if hasattr(user, 'citizenprofile'):
        return redirect('citizen:dashboard')
    elif hasattr(user, 'policeofficer'):
        return redirect('police:dashboard')
    elif hasattr(user, 'postman'):
        return redirect('postman:dashboard')
    else:
        # Redirection par défaut si le type d'utilisateur n'est pas reconnu
        return redirect('home')
    
@login_required
def user_profile(request):
    user = request.user
    profile_form = None
    
    if hasattr(user, 'citizenprofile'):
        profile = user.citizenprofile
        profile_form = CitizenProfileForm(instance=profile)
    elif hasattr(user, 'policeofficer'):
        profile = user.policeofficer
        profile_form = PoliceOfficerForm(instance=profile)
    elif hasattr(user, 'postman'):
        profile = user.postman
        profile_form = PostmanForm(instance=profile)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        if profile_form:
            profile_form = profile_form.__class__(request.POST, instance=profile)
        
        if user_form.is_valid() and (not profile_form or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserProfileForm(instance=user)
    
    return render(request, 'user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })