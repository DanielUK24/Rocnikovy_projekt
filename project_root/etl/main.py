from src.create_tables import create_tables
from src.transform.transformer import Transformer
import json

config_file = "etl/config/config.json"
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

shared_config_file = "shared/config/config.json"
with open(shared_config_file, 'r', encoding='utf-8') as f:
    shared_config = json.load(f)

create_tables(config, shared_config)

print("Tables created")

transformer = Transformer(config,1)
transformer.apply_trans_all()

print("Transformation of measurement 1 completed")

transformer = Transformer(config,2)
transformer.apply_trans_all()

print("Transformation of measurement 2 completed")