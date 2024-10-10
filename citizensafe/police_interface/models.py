from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL

class PoliceOfficer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge_number = models.CharField(max_length=20, unique=True)
    rank = models.CharField(max_length=50)
    is_on_duty = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rank} {self.user.get_full_name()} - {self.badge_number}"

class Patrol(models.Model):
    officer = models.ForeignKey(PoliceOfficer, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    route = models.TextField()  # Vous pourriez stocker ici un JSON avec les points du parcours

    def __str__(self):
        return f"Patrol - {self.officer.user.get_full_name()} - {self.start_time}"

class IncidentReport(models.Model):
    AREA_CHOICES = [
        ('1', 'Central'),
        ('2', 'Rampart'),
        ('3', 'Southwest'),
        ('4', 'Hollenbeck'),
        ('5', 'Harbor'),
        ('6', 'Hollywood'),
        ('7', 'Wilshire'),
        ('8', 'West LA'),
        ('9', 'Van Nuys'),
        ('10', 'West Valley'),
        ('11', 'Northeast'),
        ('12', '77th Street'),
        ('13', 'Newton'),
        ('14', 'Pacific'),
        ('15', 'North Hollywood'),
        ('16', 'Foothill'),
        ('17', 'Devonshire'),
        ('18', 'Southeast'),
        ('19', 'Mission'),
        ('20', 'Olympic'),
        ('21', 'Topanga'),
    ]
    
    INCIDENT_TYPES = [
        ('THEFT', 'Vol'),
        ('ASSAULT', 'Agression'),
        ('VANDALISM', 'Vandalisme'),
        ('NOISE', 'Tapage'),
        ('OTHER', 'Autre'),
    ]
    
    reporting_officer = models.ForeignKey(PoliceOfficer, on_delete=models.CASCADE)
    concerned_citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incident_reports', null=True, blank=True)    
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    area = models.CharField(max_length=100, default='Unknown')
    description = models.TextField()
    location = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_incident_type_display()} - {self.location} - {self.timestamp}"
