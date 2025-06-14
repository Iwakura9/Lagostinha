from django.shortcuts import render

# Create your views here.

gabaritos = ["joão", "Fernando", "cleber"] # temporario, vai receber a tabela de gabaritos

def index(request):
    return render(request, "gabaritos/index.html", {
        "gabaritos":gabaritos
    }) # renderiza a pagina principal

def add(request):
    return render(request, "gabaritos/add.html")