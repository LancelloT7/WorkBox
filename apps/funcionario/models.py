from django.db import models

# Create your models here.

class Funcionario(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    cargo = models.CharField(max_length=100,)
    cod = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.nome} - {self.cargo} (Código: {self.cod})"