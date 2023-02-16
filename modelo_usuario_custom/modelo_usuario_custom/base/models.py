from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Usuario(AbstractUser):
    name = models.CharField(max_length=200, null=True) #sobreescrito
    email = models.EmailField(unique=True) #sobreescrito
    biografia = models.TextField(null=True) 

    USERNAME_FIELD = 'email' #sobreescrito
    REQUIRED_FIELDS = []