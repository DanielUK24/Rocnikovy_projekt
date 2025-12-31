from src.extract.CSVExtractor import CSVExtractor
from src.transform.select_chosen_columns import select_chosen_columns
from src.transform.format_timestamps import format_timestamps
from dateutil import parser # dtd probably can be delete
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
      
      def _load_config(self, config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                  return json.load(f)

      def _create_chunk_accumulators(self):
            active_measurement_type = self._config["measurements"][self._active_measurement]["type"]
            source_codelist_id = self._config["measurements"][self._active_measurement]["target_dimensions"][0]["source_codelist_id"]
            codelist_path = self._config["codelists"][source_codelist_id]["path"]
            codelist_extractor = CSVExtractor(codelist_path)

            chunk_accumulators = {}

            join_column_codelist = self._config["measurements"][0]["target_dimensions"][0]["join_column_codelist"]
            codelist_accumulator_keys_column = self._config["measurements"][0]["target_dimensions"][0]["codelist_accumulator_keys_column"]

            while True:
                  row = codelist_extractor.get_next_row()
                  if not row:
                        break
                  if row[join_column_codelist] == active_measurement_type:
                        chunk_accumulators[row[codelist_accumulator_keys_column]] = []

            codelist_extractor.close()
            return chunk_accumulators

      def _time_difference(self, t1, t2):
           dt1 = parser.parse(t1)
           dt2 = parser.parse(t2)
           return abs(dt2 - dt1)

      def _calculate_common_difference(self, rows):
            dif_count = {}
            prev = rows[0]["Measurement Timestamp"]
            for row in rows[1::]:
                  act = row["Measurement Timestamp"]
                  dif = self._time_difference(prev, act)
                  dif_count[dif] = dif_count.get(dif, 0) + 1
                  prev = act
            print(dif_count)
            return max(dif_count, key=dif_count.get)

      def apply_trans_all(self):
            #TO DO: involve "accumulator: "yes""
            #if self._config["measurements"][self._active_measurement]["target_dimensions"][0]["accumulator"] == "yes":
            chunk_accumulators = self._create_chunk_accumulators()
            join_column_measurements = self._config["measurements"][self._active_measurement]["target_dimensions"][0]["join_column_measurements"]
            chunk_size = self._config["chunk_size"]
            
            while True:
                  row = self._extractor.get_next_row()
                  if not row:
                        break
                  chunk_accumulators[row[join_column_measurements]].append(row)
                  if len(chunk_accumulators[row[join_column_measurements]]) >= chunk_size:
                        
                        # transformations
                        chunk = select_chosen_columns(chunk_accumulators[row[join_column_measurements]], self._config["measurements"][self._active_measurement]["target_facts"]["source_columns"])

                        time_source_column = self._config["measurements"][self._active_measurement]["target_dimensions"][1]["source_column"]
                        chunk = format_timestamps(chunk, time_source_column)
                        chunk = sorted(chunk, key=lambda d: d[time_source_column], reverse=True)

                        

                        print(chunk,"\n\n\n\n\n")

                        # empty accumulator
                        del chunk_accumulators[row[join_column_measurements]][:]

                  
            for accumulator in chunk_accumulators.values():
                  if len(accumulator) > 0:
                        # start transformations
                        pass
            
            self._extractor.close()
