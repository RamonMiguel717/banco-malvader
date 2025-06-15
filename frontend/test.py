import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.utils.auxiliares import Auxiliares

print(Auxiliares.limpar_cpf("123.456.789-00"))