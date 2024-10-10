from django import forms
from django.contrib.auth.models import User
from citizen_interface.models import CitizenProfile
from police_interface.models import PoliceOfficer
from postman_interface.models import Postman

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CitizenProfileForm(forms.ModelForm):
    class Meta:
        model = CitizenProfile
        fields = ['address', 'phone_number']  # Ajoutez d'autres champs spécifiques aux citoyens

class PoliceOfficerForm(forms.ModelForm):
    class Meta:
        model = PoliceOfficer
        fields = ['badge_number', 'rank']  # Ajoutez d'autres champs spécifiques aux policiers

class PostmanForm(forms.ModelForm):
    class Meta:
        model = Postman
        fields = ['employee_id']  # Ajoutez d'autres champs spécifiques aux facteurs