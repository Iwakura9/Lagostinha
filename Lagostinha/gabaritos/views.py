import requests  # Importa a biblioteca para fazer requisições HTTP
from django.conf import settings  # Para acessar as configurações do projeto
from django.shortcuts import render
from .forms import AlunoForm
from core.models import *
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage

# Create your views here.

base_url = "http://127.0.0.1:8000/api/"

def index(request):
    # melhoria possivel

    erro = None
    try:
        response = requests.get(base_url + "leituras/")
        response.raise_for_status()
        leituras = response.json()
        saidas = []
        for leitura in leituras:
            if(leitura["erro"]): # gabarito com erro
                continue
            my_dict = {}
            my_dict["id"] = leitura["id"]
            my_dict["nota"] = leitura["nota"]
            try:
                response_part = requests.get(base_url + "participantes/" + str(leitura["participante"]))
                response_part.raise_for_status()
                leitura_part = response_part.json()
                my_dict["nome_part"] = leitura_part["nome"]

                response_prova = requests.get(base_url + "provas/" + str(leitura["prova"]))
                response_prova.raise_for_status()
                leitura_prova = response_prova.json()
                my_dict["id_prova"] = leitura_prova["id_prova"]

                response_escola = requests.get(base_url + "escolas/" + str(leitura_part["escola"]))
                response_escola.raise_for_status()
                leitura_escola = response_part.json()
                my_dict["nome_escola"] = leitura_escola["nome"]
            except Exception as inner_e:
                print(f"Inner error: {inner_e}")
                continue  


            saidas.append(my_dict)

    except Exception as e:
        saida = []
        print("erro", e)

    return render(request, "gabaritos/index.html", {
        "saidas" : saidas
    })
    
def remover(request):
    if request.method == "POST":
        leitura_id = request.POST.get('leitura-id')
        try:
            headers = {'X-CSRFToken': request.COOKIES.get('csrftoken', '')}
            response = requests.delete(base_url + "leituras/" + leitura_id + "/", headers=headers)
            response.raise_for_status()
        except Exception as e:
            print("erro", e)
    return redirect("index")

def processar_imagem(request):
    if request.method == "POST":
        try:
            if 'imagem' in request.FILES:
                
                files = {'imagem': request.FILES['imagem']}
                headers = {'Authorization': 'Token YOUR_API_TOKEN'}  
                
                
                api_url = 'http://localhost:8000/api/upload-gabarito/'  
                response = requests.post(api_url, files=files, headers=headers)
                
                if response.status_code == 201:
                    
                    data = response.json()
                    return render(request, 'gabaritos/resultado.html', {
                        'leitura': data,
                        'sucesso': True
                    })
                else:
                   
                    return render(request, 'gabaritos/add.html', {
                        'erro': 'Erro no processamento',
                        'mensagem': response.json().get('erro', 'Erro desconhecido')
                    })
        
        except Exception as e:
            print("Erro:", str(e))
            return render(request, 'gabaritos/add.html', {
                'erro': 'Erro interno',
                'mensagem': str(e)
            })

    return render(request, 'gabaritos/add.html')

def add(request):
    if request.method == 'POST':
        
        aluno = request.POST.get('aluno')
        escola = request.POST.get('escola')
        inscricao = request.POST.get('inscricao')
        
        # Coletar respostas das questões (1 a 20)
        respostas = {}
        for i in range(1, 21):
            respostas[f'questao{i}'] = request.POST.get(f'questao{i}')

        

    return render(request, 'gabaritos/add.html')
