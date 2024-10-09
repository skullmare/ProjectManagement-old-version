from django.db import models
from user.models import CustomUser

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    leaders = models.ManyToManyField(CustomUser, related_name='led_projects')
    participants = models.ManyToManyField(CustomUser, related_name='participated_projects')

    def __str__(self):
        return self.name