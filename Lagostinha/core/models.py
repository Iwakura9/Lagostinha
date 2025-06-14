from django.db import models

# Create your models here.

# cria registros de escolas no banco de dados
# cada registro é uma linha, com o nome e a cidade
class Escola(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nome} ({self.cidade})"
    
# Mesma coisa, porém para os participantes da prova
class Participante(models.Model):
    id_participante = models.IntegerField(unique=True) # Cria um id unico para cada participante, que não pode ser repetir
    
    # Já aqui criamos um campo para associar acada estudante com uma escola, deletando o aluno caso a escola seja deletada
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE) 
    
    def __str__(self): # função para que possamos ver de forma mais limpa dados dos participantes
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
    
    # NOTA: Coloquei na maioria dos campos que precisava de tamanho o tamanho 100
    # aparentemente é uma convenção, mas que podemos aumentar caso nescessário