from django import forms
from core.models import *

class AlunoForm(forms.Form):
    nome_aluno = forms.CharField(
        label="Nome do Aluno",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nome completo'})
    )
    
    nome_escola = forms.CharField(
        label="Escola",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nome da escola'})
    )
