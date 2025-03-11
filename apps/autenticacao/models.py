from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.

class Usuario(AbstractUser):

    nivel_de_acesso = models.IntegerField(default=1)
    
    def __str__(self):
        return self.username
    
  