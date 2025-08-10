from django import forms
from .models import RegistroPonto

class RegistroPontoForm(forms.ModelForm):
    class Meta:
        model = RegistroPonto
        fields = ['tipo']
        widgets = {
            'tipo': forms.RadioSelect(choices=RegistroPonto.TIPOS_REGISTRO)
        }