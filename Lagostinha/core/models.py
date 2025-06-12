from django.db import models

# Create your models here.
class Escola(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nome} ({self.cidade})"
    
    
class Participante(models.Model):
    nome = models.CharField(max_length=100)
    id_participante = models.IntegerField(unique=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nome} - {self.id_participante}"
    
class Prova(models.Model):
    id_prova = models.IntegerField(unique=True)
    gabarito = models.CharField(max_length=100)
    pesos = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Prova {self.id_prova}"
    
class Leitura(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    leitura = models.CharField(max_length=100)
    nota = models.FloatField()
    erro = models.IntegerField() # 0: ok, 1: erro
    
    def __str__(self):
        return f"Leitura de {self.participante} na {self.prova}"