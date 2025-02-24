from django.contrib import admin
from apps.funcionario.models import Funcionario

# Register your models here.
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display =('nome', 'cargo')