from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .leitor import ler_gabarito
from .models import Escola, Participante, Prova, Leitura
from .serializers import EscolaSerializer, ParticipanteSerializer, ProvaSerializer, LeituraSerializer
import tempfile

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

# View para upload de gabarito e leitura de imagem.
# Essa view recebe uma imagem, processa-a e retorna os resultados da leitura.
class GabaritoUploadView(APIView):
    def post(self, request, *args, **kwargs):
        imagem = request.FILES.get('imagem')

        if not imagem:
            return Response({"erro": "Nenhuma imagem enviada"}, status=status.HTTP_400_BAD_REQUEST)


        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
            for chunk in imagem.chunks():
                temp.write(chunk)
            temp.flush()
            leitura = ler_gabarito(temp.name)


        if leitura.erro != 0:
            return Response({
                "erro": leitura.erro,
                "mensagem": "Erro na leitura da imagem. Código de erro diferente de 0.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            prova = Prova.objects.get(pk=leitura.id_prova)
            participante = Participante.objects.get(pk=leitura.id_participante)
        except (Prova.DoesNotExist, Participante.DoesNotExist):
            return Response({"erro": "Prova ou participante não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Calcula a nota
        gabarito = list(prova.gabarito)
        respostas = list(leitura.leitura.decode())
        pesos = list(map(int, prova.pesos.split(',')))

        nota = 0
        for g, r, p in zip(gabarito, respostas, pesos):
            if g == r:
                nota += p

        leitura_obj = Leitura.objects.create(
            participante=participante,
            prova=prova,
            leitura=leitura.leitura.decode(),
            nota=nota,
            erro=leitura.erro,
        )

        serializer = LeituraSerializer(leitura_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
