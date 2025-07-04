"""
URL configuration for Lagostinha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django .conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
"""
adiciona uma configuração para servir arquivos de mídia durante o 
desenvolvimento. Serve para acessar arquivos de mídia que são 
carregados pelos usuários. O `settings.MEDIA_URL` define a 
URL base para acessar esses arquivos, enquanto `settings.MEDIA_ROOT` 
especifica o diretório no sistema de arquivos onde esses arquivos estão armazenados.
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Inclui as URLs da aplicação core
    # assim os endpoints da API estarão disponíveis sob /api/
    path('gabaritos/', include('gabaritos.urls')),  # Inclui as URLs da interfaces
    # que serão de fato acessadas
    path('',RedirectView.as_view(url='gabaritos/', permanent=True))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

