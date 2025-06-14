from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add, name="add") # está a mesma função por enquanto, altararei depois
]