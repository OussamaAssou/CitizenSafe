from django import forms
from .models import Patrol, IncidentReport, PoliceOfficer
from django.contrib.auth import get_user_model

User = get_user_model()

def get_citizen_choices():
    return [(user.id, f"{user.first_name} {user.last_name}") for user in User.objects.filter(user_type='citizen')]  

class PatrolForm(forms.ModelForm):
    class Meta:
        model = Patrol
        fields = ['start_time', 'end_time', 'route']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'route': forms.Textarea(attrs={'rows': 3}),
        }

class IncidentReportForm(forms.ModelForm):
    concerned_citizen = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='citizen'),
        label="Citoyen concerné",
        empty_label="Sélectionnez un citoyen",
        to_field_name="id",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = IncidentReport
        fields = ['incident_type', 'description', 'location', 'timestamp', 'concerned_citizen']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concerned_citizen'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

class PoliceOfficerForm(forms.ModelForm):
    class Meta:
        model = PoliceOfficer
        fields = ['badge_number', 'rank', 'is_on_duty']