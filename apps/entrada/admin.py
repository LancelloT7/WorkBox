from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('ptn', 'serie', 'sku', 'modelo', 'responsavel_entrada', 'data_entrada', 'impresso',)
    search_fields = ('ptn', 'serie', 'sku', 'modelo')
    list_filter = ('status', 'responsavel_entrada')
    ordering = ('data_entrada',)