from django.contrib import admin
from .models import RegistroPonto

@admin.register(RegistroPonto)
class RegistroPontoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'data_hora', 'endereco')
    list_filter = ('tipo', 'usuario')
    search_fields = ('usuario__username', 'endereco')