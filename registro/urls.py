from django.urls import path
from . import views

urlpatterns = [
    path('registrar-ponto/', views.registrar_ponto, name='registrar_ponto'),
    path('registros-hoje/', views.get_registros_hoje, name='get_registros_hoje'),
    path('', views.home, name='home'),
    path('historico-pontos/', views.historico_pontos, name='historico_pontos'),

    # Outras URLs do seu app...
]
