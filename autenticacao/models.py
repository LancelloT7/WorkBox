from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password

# Create your models here.

class Usuario(AbstractUser):

    groups = models.ManyToManyField(Group, related_name="usuario_autenticacao_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="usuario_autenticacao_permissions")
    nivel_de_acesso = models.IntegerField(default=1)
    
    def __str__(self):
        return self.username
    
  