from django.contrib import admin
from .models import Peca, ProdutoPeca
from sku.models import Sku,Sufixo

# Register your models here.
@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    search_fields = ('descricao',)
    list_display = ('descricao','sku','sufixo',)

@admin.register(ProdutoPeca)
class ProdutoPecaAdmin(admin.ModelAdmin):
    search_fields = ('numero_pedido',)
    list_display = ('numero_pedido',)

     

    