from django.db import models
from sku.models import Sku, Sufixo

# Create your models here.

class Peca(models.Model):
    STATUS_PECAS = [
        ('VERIFICAR DISPONIBILIDADE', 'VERIFICAR DISPONIBILIDADE'),
        ('AGUARDANDO PEÇA', 'AGUARDANDO PEÇA'),
        ('LIBERADO PARA CONSERTO', 'LIBERADO PARA CONSERTO'),
    ]
    DEFEITO_PECAS = [

        ('ND',' ' ),
        ('NÃO LIGA','NÃO LIGA' ),
        ('RISCADO','RISCADO' ),
        ('OXIDADO','OXIDADO' ),
        ('MANCHADO','MANCHADO' ),
        ('FALTANTE','FALTANTE' ),

    ]

    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name="pecas")
    sufixo = models.ForeignKey(Sufixo, on_delete=models.CASCADE, related_name="pecas")
    part_number = models.CharField(max_length=15, null=False, blank=False)
    status = models.CharField(max_length=30, choices=STATUS_PECAS, default="VERIFICAR DISPONIBILIDADE")
    defeito_pecas = models.CharField(choices=DEFEITO_PECAS, max_length=255, null=True, blank=True, default="ND")
    posicao =  models.CharField(max_length=15, null=False, blank=False)
    descricao = models.CharField(max_length=100, null=False, blank=False)  
    observacao = models.TextField(blank=True, null=True)  


    def __str__(self):
        return f"SKU: {self.sku.sku} | Sufixo: {self.sufixo.sufixo} | PN: {self.part_number} | Status: {self.status} | dEFEITO: {self.defeito_pecas}"

