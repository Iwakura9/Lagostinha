import os
import ctypes
from pathlib import Path

# 1. Localiza a raiz do projeto (duas pastas acima de leitor.py)
BASE_DIR = Path(__file__).resolve().parents[1]  
#    └─ parents[0] seria /core
#       parents[1] é /Lagostinha (a raiz do repositório)

# 2. Define o diretório onde estão as bibliotecas .so
LIB_DIR = BASE_DIR / "bin"

# 3. Opcional: garante que o sistema saiba onde achar as libs dependentes
os.environ["LD_LIBRARY_PATH"] = str(LIB_DIR) + (
    ":" + os.environ.get("LD_LIBRARY_PATH", "")
)

# 4. Caminho completo para a biblioteca principal
LIB_PATH = LIB_DIR / "libleitor.so"

# 5. Carrega a biblioteca com ctypes
try:
    leitor = ctypes.CDLL(str(LIB_PATH))
except OSError as e:
    raise OSError(
        f"Não foi possível carregar {LIB_PATH!s}. "
        f"Verifique se a pasta 'bin/' está na raiz e contém libleitor.so e todas as dependências. "
        f"Erro original: {e}"
    )

# 6. Define o struct Reading conforme o header C++
class Reading(ctypes.Structure):
    _fields_ = [
        ("erro", ctypes.c_int),
        ("id_prova", ctypes.c_int),
        ("id_participante", ctypes.c_int),
        ("leitura", ctypes.c_char_p),
    ]

# 7. Configura os tipos de argumento e retorno
leitor.read_image_path.argtypes = [ctypes.c_char_p]
leitor.read_image_path.restype = Reading

def ler_gabarito(path_imagem: str) -> Reading:
    path = Path(path_imagem).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Arquivo {path} não encontrado.")
    return leitor.read_image_path(str(path).encode())

