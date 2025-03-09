from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.

class Usuario(models.Model):

    nome = models.CharField(max_length=20, unique=True, null=False, blank=False)
    senha = models.CharField(max_length=20, unique=True, null=False, blank=False)
    

    def __str__(self):
        return self.nome
    
    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
