from src.extract.CSVExtractor import CSVExtractor

extractor = CSVExtractor("C:/Users/danie/Documents/matfyz_3_semester/rocnikovy_projekt/git clone/Rocnikovy_projekt/project_root/data/raw/Beach_Water_Quality_-_Automated_Sensors_20251016.csv")

extractor.getInitialChunk()

while True:
    chunk = extractor.getChunk()
    if not chunk:
        break
    print(chunk)

extractor.close()