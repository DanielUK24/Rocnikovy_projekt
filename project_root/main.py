from src.create_tables import create_tables
from src.transform.transformer import Transformer
import json

config_file = "config/config.json"
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

create_tables(config)
transformer = Transformer(config,0)
transformer.apply_trans_all()

print("here")

transformer = Transformer(config,1)
transformer.apply_trans_all()

print("here")

transformer = Transformer(config,2)
transformer.apply_trans_all()
