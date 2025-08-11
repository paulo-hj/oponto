from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import RegistroPonto
import json
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

@login_required
def home(request):
    """
    View para a página inicial
    """
    return render(request, 'registro/home.html', {
        'user': request.user,
        'hoje': timezone.localdate()  # Passa a data atual para o template
    })

@login_required
@csrf_exempt  # Remover em produção
def registrar_ponto(request):
    """
    View para registrar um novo ponto
    """
    logger.info(f"Requisição de registro recebida - Método: {request.method}")
    
    if request.method != "POST":
        logger.warning("Tentativa de acesso com método não permitido")
        return JsonResponse({
            "success": False,
            "error": "Método não permitido"
        }, status=405)

    try:
        # Decodifica e valida os dados
        data = json.loads(request.body.decode('utf-8'))
        logger.debug(f"Dados recebidos: {data}")
        
        # Campos obrigatórios
        required_fields = ['tipo', 'latitude', 'longitude']
        if not all(field in data for field in required_fields):
            missing = [f for f in required_fields if f not in data]
            logger.warning(f"Campos obrigatórios faltando: {missing}")
            return JsonResponse({
                "success": False,
                "error": f"Campos obrigatórios faltando: {', '.join(missing)}"
            }, status=400)

        # Cria e valida o registro
        registro = RegistroPonto(
            usuario=request.user,
            tipo=data['tipo'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            endereco=data.get('endereco', ''),
            data_hora=timezone.now()
        )
        
        registro.full_clean()  # Validação do modelo
        registro.save()
        
        logger.info(f"Ponto registrado com sucesso - ID: {registro.id}")
        
        return JsonResponse({
            "success": True,
            "message": "Ponto registrado com sucesso!",
            "id": registro.id
        })

    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {str(e)}")
        return JsonResponse({
            "success": False,
            "error": "Formato de dados inválido"
        }, status=400)
        
    except ValueError as e:
        logger.error(f"Valor inválido recebido: {str(e)}")
        return JsonResponse({
            "success": False,
            "error": "Coordenadas inválidas"
        }, status=400)
        
    except ValidationError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)
        
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        return JsonResponse({
            "success": False,
            "error": "Erro interno no servidor"
        }, status=500)

@login_required
def get_registros_hoje(request):
    """Retorna todos os registros do usuário para o dia atual"""
    try:
        # Obtém a data atual considerando o fuso horário
        hoje = timezone.localdate()
        
        # Consulta otimizada ao banco de dados
        registros = RegistroPonto.objects.filter(
            usuario=request.user,
            data_hora__date=hoje
        ).order_by('data_hora').values(
            'id',
            'tipo',
            'data_hora',
            'latitude',
            'longitude',
            'endereco'
        )
        
        # Converte o QuerySet para lista
        registros_list = list(registros)
        
        # registerPointormata as datas
        for registro in registros_list:
            registro['data_hora'] = registro['data_hora'].isoformat()
        
        return JsonResponse({
            "success": True,
            "data": registros_list,
            "count": len(registros_list),
            "date": hoje.isoformat()
        }, safe=False)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

@login_required
def historico_pontos(request):
    try:
        # Obtém parâmetros de data
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Filtra os registros
        queryset = RegistroPonto.objects.filter(
            usuario=request.user
        ).order_by('-data_hora')
        
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(
                data_hora__date__range=[start_date, end_date]
            )
        
        # Serializa os dados
        registros = list(queryset.values(
            'id',
            'tipo',
            'data_hora',
            'endereco'
        ))
        
        return JsonResponse({
            'success': True,
            'data': registros
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)