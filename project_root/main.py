from pathlib import Path
from src.transform.transformer import Transformer

transformer = Transformer("config/config.json")
print("\n\n\n")
transformer.apply_trans_all()