from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Postman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    route = models.TextField()  # Vous pourriez stocker ici un JSON avec les points du parcours
    is_on_duty = models.BooleanField(default=False)

    def __str__(self):
        return f"Postman - {self.user.get_full_name()} - {self.employee_id}"

class Observation(models.Model):
    OBSERVATION_TYPES = [
        ('SUSPICIOUS', 'Activité suspecte'),
        ('SAFETY', 'Problème de sécurité'),
        ('MAINTENANCE', 'Problème de maintenance'),
        ('OTHER', 'Autre'),
    ]
    
    postman = models.ForeignKey(Postman, on_delete=models.CASCADE)
    concerned_citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='postman_observations', null=True, blank=True)
    observation_type = models.CharField(max_length=20, choices=OBSERVATION_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_observations')

    def __str__(self):
        return f"{self.get_observation_type_display()} - {self.postman.user.get_full_name()} - {self.timestamp}"
