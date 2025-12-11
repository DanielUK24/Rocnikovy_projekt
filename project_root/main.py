from pathlib import Path
from src.extract.CSVExtractor import CSVExtractor

csv_file_path = Path(__file__).parent / "data" / "raw" / "chybajuce_cele_zaznamy_v01_input01.csv"
extractor = CSVExtractor(csv_file_path)

while True:
    chunk = extractor.get_next_chunk()
    if not chunk:
        break
    print(chunk,"\n\n\n\n\n")

extractor.close()