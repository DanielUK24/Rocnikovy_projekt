from pathlib import Path
from src.transform.transformer import Transformer

transformer = Transformer("config/config.json")
transformer.apply_trans_all()