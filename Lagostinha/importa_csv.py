import csv
from core.models import Escola, Prova, Participante

# Importar Escolas
with open("escolas.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Escola.objects.update_or_create(id=row['id'], defaults={"nome": row['nome']})
print("Escolas importadas.")

# Importar Provas
with open("provas.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Prova.objects.update_or_create(
            id=row['id'],
            defaults={
                "nome": row["nome"],
                "gabarito": row["gabarito"],
                "pesos": row["pesos"],
            }
        )
print("Provas importadas.")

# Importar Participantes
with open("participantes.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        escola = Escola.objects.get(pk=row['escola'])
        Participante.objects.update_or_create(
            id=row['id'],
            defaults={
                "nome": row["nome"],
                "escola": escola
            }
        )
print("Participantes importados.")
