from rest_framework import serializers
from .models import Escola, Participante, Prova, Leitura

"""
Serializers para os modelos Escola, Participante, Prova e Leitura.
Permitem converter instâncias dos modelos para JSON e vice-versa,
facilitando a comunicação entre a API e o frontend.
"""

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'
        
class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'
        
class ProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prova
        fields = '__all__'
        
class LeituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leitura
        fields = '__all__'
        
