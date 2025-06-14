from django import forms
from core.models import Escola, Participante, Prova, Leitura

class ParticipanteForms(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome']
        label = {
            'nome' : "nome do aluno: "
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'nome'}),
        }
        