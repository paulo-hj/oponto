from django.db import models
from django.contrib.auth.models import User

class RegistroPonto(models.Model):
    TIPOS_REGISTRO = [
        ('entrada', 'Entrada'),
        ('intervalo', 'Intervalo'),
        ('retorno', 'Retorno'),
        ('saida', 'Saída'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_REGISTRO)
    data_hora = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    endereco = models.TextField()

    class Meta:
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()} - {self.data_hora}"