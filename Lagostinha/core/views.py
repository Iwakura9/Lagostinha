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

from django.shortcuts import render
from rest_framework import viewsets
from .models import Escola, Participante, Prova, Leitura
from .serializers import EscolaSerializer, ParticipanteSerializer, ProvaSerializer, LeituraSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.core.files.storage import default_storage
from .leitor import ler_gabarito
from .models import Leitura, Prova, Participante


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


class GabaritoUploadView(APIView):
    parser_classes = [MultiPartParser]  # Permite o upload de arquivos
    
    def post(self, request):
        if 'imagem' not in request.FILES:
            return Response({"error": "Nenhum arquivo enviado."}, status=400)
        
        imagem = request.FILES['imagem']
        caminho = default_storage.save(f'uploads/{imagem.name}', imagem)
        caminho_absoluto = default_storage.path(caminho)
        
        resultado = ler_gabarito(caminho_absoluto)
        
        # Lê informações do retorno da lib
        erro = resultado.erro
        id_prova = resultado.id_prova
        id_participante = resultado.id_participante
        leitura = resultado.leitura.decode()
        
        # proucura objetos no banco de dados
        try:
            participante = Participante.objects.get(id_participante=id_participante)
            prova = Prova.objects.get(id_prova=id_prova)
        except (Participante.DoesNotExist, Prova.DoesNotExist):
            return Response({"error": "Participante ou Prova não encontrados."}, status=404)
        
        # Calcula a nota
        pesos = list(map(int, prova.pesos.split(',')))
        gabarito = prova.gabarito
        nota = calcular_nota(leitura, gabarito, pesos)
        
        # Salva no banco de dados
        leitura_obj = Leitura.objects.create(
            participante=participante,
            prova=prova,
            leitura=leitura,
            erro=erro,
            nota=nota
        )
        
        return Response({
            'leitura': leitura,
            'erro': erro,
            'id_participante': id_participante,
            'id_prova': id_prova,
        }, status=201)
        
def calcular_nota(leitura: str, gabarito: str, pesos: list[int]) -> float:
    total = 0.0
    for resposta, correta, peso in zip(leitura, gabarito, pesos):
        if resposta == correta:
            total += peso
    return total
