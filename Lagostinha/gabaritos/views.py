from django.shortcuts import render
from .forms import ParticipanteForms

# Create your views here.

gabaritos = ["joão", "Fernando", "cleber"] # temporario, vai receber a tabela de gabaritos

def index(request):
    return render(request, "gabaritos/index.html", {
        "gabaritos":gabaritos
    }) # renderiza a pagina principal

def add(request):
    if request.method == 'post':
        form = ParticipanteForms(request.POST)
        # salvar a informação
        
    else:
        form = ParticipanteForms()
    return render(request, "gabaritos/add.html", {'form' : form})
