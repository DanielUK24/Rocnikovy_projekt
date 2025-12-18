from src.extract.CSVExtractor import CSVExtractor
from dateutil import parser
import json

class Transformer:

      def __init__(self, config_file):

           #self._chunk_size = self._config.get("chunk_size")
           #if self._chunk_size is None:
            #raise ValueError("chunk_size must be specified in config.json")
           
           self._config = self._load_config(config_file)
           self._active_measurement = self._config.get("active_measurement")
           active_measurement_path = self._config.get("measurements")[self._active_measurement].get("path")
           self._extractor = CSVExtractor(active_measurement_path)

      def _create_chunk_accumulators(self):
            active_measurement_type = self._config.get("measurements")[self._active_measurement].get("type")
            codelist_path = self._config.get("codelists")[0].get("path")
            codelist_extractor = CSVExtractor(codelist_path)

            chunk_accumulators = {}

            while True:
                  row = codelist_extractor.get_next_row()
                  if not row:
                        break
                  if row[0].get("Sensor Type") == active_measurement_type:
                        chunk_accumulators[row[0].get("Sensor Name")] = {}

            codelist_extractor.close()
            return chunk_accumulators


      def _load_config(self, config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)

      def _time_difference(self, t1, t2):
           dt1 = parser.parse(t1)
           dt2 = parser.parse(t2)
           return abs(dt2 - dt1)

      def _calculate_common_difference(self, lines):
            dif_count = {}
            prev = lines[0]["Measurement Timestamp"]
            for line in lines[1::]:
                  act = line["Measurement Timestamp"]
                  dif = self._time_difference(prev, act)
                  dif_count[dif] = dif_count.get(dif, 0) + 1
                  prev = act
            print(dif_count)
            return max(dif_count, key=dif_count.get)

      def apply_trans_all(self):
            print(self._create_chunk_accumulators())
            
            
            self._extractor.close()

