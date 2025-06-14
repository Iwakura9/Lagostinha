import requests  # Importa a biblioteca para fazer requisições HTTP
from django.conf import settings  # Para acessar as configurações do projeto
from django.shortcuts import render


# Create your views here.

gabaritos = ["joão", "Fernando", "cleber"] # temporario, vai receber a tabela de gabaritos

def index(request):
    try:
        response = requests.get(f'{settings.API_BASE_URL}/participantes/')
        response.raise_for_status() 
        participantes = response.json()

    except requests.exceptions.RequestException as e:
        participantes = []

    return render(request, "gabaritos/index.html", {
        "participantes": participantes
    })
    

def add(request):
    
    return render(request, "gabaritos/add.html")
