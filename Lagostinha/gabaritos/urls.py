from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add', views.add, name="add") #
    path('remove', views.remover, name="remove")
]
