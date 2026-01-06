import sys
from pathlib import Path

# Adiciona a raiz do projeto ao PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
