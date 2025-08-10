from django.shortcuts import render

def home(request):
    return render(request, 'registro/home.html', {
        'title': 'Oponto - Sistema de Ponto Eletrônico',
        'ip': '192.168.1.230'
    })
