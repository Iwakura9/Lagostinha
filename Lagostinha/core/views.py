from django.shortcuts import render
from rest_framework import viewsets
from .models import Escola, Participante, Prova, Leitura
from .serializers import EscolaSerializer, ParticipanteSerializer, ProvaSerializer, LeituraSerializer

# Views para os modelos Escola, Participante, Prova e Leitura.
'''
 - Lembrar:
list: GET /recurso/
create: POST /recurso/
retrieve: GET /recurso/{id}/
update: PUT /recurso/{id}/
partial_update: PATCH /recurso/{id}/
destroy: DELETE /recurso/{id}/
'''

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all() # QuerySet que retorna todas as instâncias de Escola
    serializer_class = EscolaSerializer # Serializer que define como os dados serão convertidos para JSON, nesse caso os dados da Escola
    
class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer   
    
class ProvaViewSet(viewsets.ModelViewSet):
    queryset = Prova.objects.all()
    serializer_class = ProvaSerializer  
    
class LeituraViewSet(viewsets.ModelViewSet):
    queryset = Leitura.objects.all()
    serializer_class = LeituraSerializer


