import csv
import json
from pathlib import Path

class CSVExtractor:
    def __init__(self, csv_file_path):
        
        self._file = open(csv_file_path, mode = 'r', newline='', encoding='utf-8')
        reader = csv.DictReader(self._file)
        self._iterator = iter(reader)

    def get_next_row(self):
        row = []
        try:
            row.append(next(self._iterator))
        except StopIteration:
            pass
        return row if row else None
    
    def close(self):
        self._file.close()
        