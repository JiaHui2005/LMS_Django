from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES=(
        ('manager', 'Manager'),
        ('lecturer', 'Lecturer'),
        ('coordinator', 'Coordinator'),
        ('cs', 'Customer Support'),
        ('student', 'Student'),
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    
    full_name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name} ({self.role})"
    