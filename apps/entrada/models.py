from django.db import models
from produto.models import Produto

# Create your models here.

class Entrada(models.Model):

    numero_entrada = models.IntegerField(auto_created=True, default=100)
    produtos_entrada = models.ManyToManyField(Produto, related_name="produtos_entrada")

    def __str__(self):
        return self.numero_entrada, self.produtos_entrada

