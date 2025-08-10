from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RegistroPonto(models.Model):
    TIPOS_REGISTRO = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
        ('I', 'Intervalo'),
        ('R', 'Retorno'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=1, choices=TIPOS_REGISTRO, default='E')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-data_hora']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()} - {self.data_hora}"