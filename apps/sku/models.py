from django.db import models

# Create your models here.



class Sku(models.Model):
    sku = models.IntegerField(unique=True,)
    modelo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"SKU: {self.sku}"

class Sufixo(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name="sku_sufixo")
    sufixo = models.CharField(max_length=100, unique=False)

    def __str__(self):
        return f"{self.sku} - {self.sufixo}"