import ctypes
from pathlib import Path

# definimos a estrutura reading, deixando igual ao da biblioteca 
class Reading(ctypes.Structure):
    _fields_ = [
        ("erro", ctypes.c_int),
        ("id_prova", ctypes.c_int),
        ("id_participante", ctypes.c_int),
        ("leitura", ctypes.c_char_p)
    ]
    
# caminho para a biblioteca libleitor.so
LIB_PATH = Path(__file__).resolve().parent /bin/"libleitor.so"
leitor = ctypes.CDLL(str(LIB_PATH))

# tipos de argumentos e retorno da função read_image_path
leitor.read_image_path.argtypes = [ctypes.c_char_p]
leitor.read_image_path.restype = Reading

# função para usar o libleitor.so
def ler_gabarito(path_imagem: str) -> Reading:
    resultado = leitor.read_image_path(path_imagem.encode())
    return resultado



