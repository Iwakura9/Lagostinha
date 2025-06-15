import csv
from core.models import Escola, Participante, Prova

# 🏫 Importar escolas e participantes
escolas_cache = {}  # evita recriar a mesma escola

with open("participantes.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        escola_nome = row['escola']
        if escola_nome not in escolas_cache:
            escola_obj, _ = Escola.objects.get_or_create(nome=escola_nome)
            escolas_cache[escola_nome] = escola_obj
        else:
            escola_obj = escolas_cache[escola_nome]

        Participante.objects.update_or_create(
            id=row['id'],
            defaults={
                'nome': row['nome'],
                'escola': escola_obj
            }
        )
print("Participantes e escolas importados.")

# 📝 Importar provas com pesos = 1,1,1,... com base no gabarito
with open("provas.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gabarito = row['Gabarito'].strip().lower()
        pesos = ",".join(["1"] * len(gabarito))  # gera 1,1,1,... com mesmo tamanho do gabarito

        Prova.objects.update_or_create(
            id=row['Prova'],
            defaults={
                'nome': f"Prova {row['Prova']}",
                'gabarito': gabarito,
                'pesos': pesos
            }
        )
print("Provas importadas.")
