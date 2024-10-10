from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('citizen', 'Citoyen'),
        ('police', 'Policier'),
        ('postman', 'Facteur'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='citizen')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CitizenProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citizenprofile')
    address = models.CharField(max_length=200)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.address}"

class Alert(models.Model):
    ALERT_TYPES = [
        ('INTRUSION', 'Intrusion'),
        ('FIRE', 'Incendie'),
        ('MEDICAL', 'Urgence médicale'),
        ('SUSPICIOUS', 'Activité suspecte'),
        ('OTHER', 'Autre'),
    ]
    
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts')

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.citizen.user.username} - {self.timestamp}"

class SafetyTip(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class AbsenceDeclaration(models.Model):
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.citizen.username} - {self.start_date} to {self.end_date}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_citizen_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'citizen':
        CitizenProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_citizen_profile(sender, instance, **kwargs):
    if instance.user_type == 'citizen':
        instance.citizenprofile.save()