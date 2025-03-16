from django.contrib import admin
from .models import Sku, Sufixo

# Register your models here.
@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    pass

@admin.register(Sufixo)
class SufixoAdmin(admin.ModelAdmin):
    pass