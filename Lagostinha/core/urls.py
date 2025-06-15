from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EscolaViewSet, ParticipanteViewSet, ProvaViewSet, LeituraViewSet, GabaritoUploadView

# URL routing para a API do Lagostinha.
router = DefaultRouter()
router.register(r'escolas', EscolaViewSet)
router.register(r'participantes', ParticipanteViewSet) 
router.register(r'provas', ProvaViewSet)
router.register(r'leituras', LeituraViewSet)
# cria automaticamente as URLs para os viewsets registrados

urlpatterns = router.urls
urlpatterns += [ 
    path('upload-gabarito/', GabaritoUploadView.as_view(), name='upload-gabarito')
]
