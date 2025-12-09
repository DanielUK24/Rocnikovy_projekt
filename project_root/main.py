from pathlib import Path
from src.extract.CSVExtractor import CSVExtractor

csv_file_path = Path(__file__).parent / "data" / "raw" / "Beach_Water_Quality_-_Automated_Sensors_20251016.csv"
extractor = CSVExtractor(csv_file_path)

while True:
    chunk = extractor.getNextChunk()
    if not chunk:
        break
    print(chunk)

extractor.close()