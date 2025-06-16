import requests  # Importa a biblioteca para fazer requisições HTTP
from django.conf import settings  # Para acessar as configurações do projeto
from django.shortcuts import render
from .forms import AlunoForm
from core.models import *

# Create your views here.

base_url = "http://127.0.0.1:8000/api/"

def index(request):
    erro = None
    try:
        response = requests.get(base_url + "leituras/")
        response.raise_for_status()
        leituras = response.json()
    except Exception as e:
        leituras = []
        print("erro", e)

    return render(request, "gabaritos/index.html", {
        "leituras" : leituras
    })

def add(request):
    mensagem = None
    tipo_mensagem = None # erro, sucesso, ou None

    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():

            nome_aluno = form.cleaned_data['nome_aluno'] 
            nome_escola = form.cleaned_data['nome_escola']
            
            try:
                # Verifica se a escola existe
                response = requests.get(
                    f'{settings.API_BASE_URL}/escolas/',
                    params={'nome__iexact': nome_escola}
                )
                response.raise_for_status()  # Verifica erros na requisição
                escolas = response.json()

                if escolas:  # Escola existe
                    escola_id = escolas[0]['id']
                    mensagem = f"Aluno vinculado à escola existente: {nome_escola}"
                else:  # Cria nova escola
                    response = requests.post(
                        f"{settings.API_BASE_URL}/escolas/",
                        json={'nome': nome_escola}
                    )
                    response.raise_for_status()
                    escola_id = response.json()['id']
                    mensagem = f"Nova escola cadastrada: {nome_escola}"
                
                # Cadastra o aluno
                response = requests.post(
                    f"{settings.API_BASE_URL}/participantes/",
                    json={
                        'nome': nome_aluno,
                        'escola': escola_id
                    }
                )
                response.raise_for_status()
                
                tipo_mensagem = 'sucesso'
                form = AlunoForm() 

            except requests.exceptions.RequestException as e:
                mensagem = "Erro na comunicação com a API:" + str(e)
                tipo_mensagem = "erro"
            except Exception as e:
                mensagem = "Erro no cadastro: " + str(e)
                tipo_mensagem = "erro"
    else:
        form = AlunoForm()
    
    return render(request, "gabaritos/add.html",{
        'form': form,
        'mensagem': mensagem,
        'tipo_mensagem': tipo_mensagem
    })
