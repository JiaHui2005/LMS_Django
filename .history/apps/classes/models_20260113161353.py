from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Class(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    lecturers = models.ManyToManyField(
        User,
        related_name='teaching_classes',
        limit_choices_to={'role': 'lecturer'}
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name