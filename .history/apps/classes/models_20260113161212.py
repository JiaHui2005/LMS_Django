from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Class(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name =