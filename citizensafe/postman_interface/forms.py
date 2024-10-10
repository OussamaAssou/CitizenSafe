from django import forms
from .models import Observation, Postman
from django.contrib.auth import get_user_model

User = get_user_model()

class ObservationForm(forms.ModelForm):
    concerned_citizen = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='citizen'),
        label="Citoyen concerné",
        required=False,
        empty_label="Sélectionnez un citoyen"
    )

    class Meta:
        model = Observation
        fields = ['observation_type', 'description', 'location', 'concerned_citizen']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concerned_citizen'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

class PostmanForm(forms.ModelForm):
    class Meta:
        model = Postman
        fields = ['employee_id', 'route', 'is_on_duty']
        widgets = {
            'route': forms.Textarea(attrs={'rows': 3}),
        }