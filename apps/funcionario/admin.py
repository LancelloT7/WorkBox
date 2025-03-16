from django.contrib import admin
from funcionario.models import Funcionario

# Register your models here.
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display =('nome', 'cargo')