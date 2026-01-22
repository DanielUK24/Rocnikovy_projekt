import csv

class CSVExtractor:
    def __init__(self, csv_file_path):
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self._rows = list(reader)

        self._index = len(self._rows) - 1

    def get_next_row(self):
        if self._index < 0:
            return None

        row = self._rows[self._index]
        self._index -= 1
        return row

    def close(self):
        pass