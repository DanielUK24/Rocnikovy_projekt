from pathlib import Path
from src.transform.Transformer import Transformer

transformer = Transformer("config/config.json")
transformer.apply_trans_all()