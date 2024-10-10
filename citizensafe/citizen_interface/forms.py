from django import forms
from .models import Alert, CitizenProfile, SafetyTip, AbsenceDeclaration, User 
from police_interface.models import PoliceOfficer
from postman_interface.models import Postman
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['alert_type', 'description', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CitizenProfileForm(forms.ModelForm):
    class Meta:
        model = CitizenProfile
        fields = ['address', 'phone_number', 'emergency_contact', 'emergency_contact_phone']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+33123456789'}),
            'emergency_contact_phone': forms.TextInput(attrs={'placeholder': '+33123456789'}),
        }

class SafetyTipForm(forms.ModelForm):
    class Meta:
        model = SafetyTip
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class AbsenceDeclarationForm(forms.ModelForm):
    class Meta:
        model = AbsenceDeclaration
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.')
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom')
    badge_number = forms.CharField(max_length=20, required=False, label='No de Badge')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['badge_number'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        badge_number = cleaned_data.get('badge_number')

        if user_type in ['police', 'postman'] and not badge_number:
            raise forms.ValidationError("Le numéro de badge est requis pour les policiers et les facteurs.")

        return cleaned_data