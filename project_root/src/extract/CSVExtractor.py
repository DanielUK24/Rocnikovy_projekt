import csv
import json
from pathlib import Path

class CSVExtractor:
    def __init__(self, csv_file_path, config_file_path = Path(__file__).resolve().parents[2] / "config" / "config.json"):

        self._csv_file_path = csv_file_path
        self._config = self._load_config(config_file_path)

        self._chunk_size = self._config.get("chunk_size")
        if self._chunk_size is None:
            raise ValueError("chunk_size must be specified in config.json")
        
        self._file = open(self._csv_file_path, mode = 'r', newline='', encoding='utf-8')
        self._reader = csv.DictReader(self._file)
        self._iterator = iter(self._reader)

    def _load_config(self, config_file_path):
            with open(config_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    def get_next_chunk(self):
        chunk = []
        try:
            for _ in range(self._chunk_size):
                chunk.append(next(self._iterator))
        except StopIteration:
            pass
        return chunk if chunk else None
    
    def close(self):
        self._file.close()
        