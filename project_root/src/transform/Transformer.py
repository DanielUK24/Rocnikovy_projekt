from src.extract.csv_extractor import CSVExtractor
from src.load.loader import Loader
from src.transform.select_source_columns import select_source_columns
from src.transform.format_timestamps import format_timestamps
from src.transform.correct_measurements import correct_measurements
from src.transform.regularize_timestamps import regularize_timestamps
from dateutil import parser
import json

class Transformer:

      def __init__(self):

           self._config = self._load_config("config/config.json")
           self._active_measurement = self._config.get("active_measurement")
           active_measurement_path = self._config.get("measurements")[self._active_measurement].get("path")
           self._extractor = CSVExtractor(active_measurement_path)
           self._regularize_bool = False
           self._correct_bool = False
      
      def _load_config(self, config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                  return json.load(f)

      def _create_chunk_accumulators(self):
            type = self._config["measurements"][self._active_measurement]["type"]
            source_codelist_id = self._config["measurements"][self._active_measurement]["target_dimensions"][0]["source_codelist_id"]
            codelist_path = self._config["codelists"][source_codelist_id]["path"]
            codelist_extractor = CSVExtractor(codelist_path)

            chunk_accumulators = {}

            join_column_codelist = self._config["measurements"][0]["target_dimensions"][0]["join_column_codelist"]
            sensor_name_column_codelist = self._config["measurements"][0]["target_dimensions"][0]["sensor_name_column_codelist"]

            while True:
                  row = codelist_extractor.get_next_row()
                  if not row:
                        break
                  if row[join_column_codelist] == type:
                        chunk_accumulators[row[sensor_name_column_codelist]] = []

            codelist_extractor.close()
            return chunk_accumulators

      def _time_difference(self, t1, t2):
           dt1 = parser.parse(t1)
           dt2 = parser.parse(t2)
           return abs(dt2 - dt1)

      def _calculate_common_difference(self, chunk, join_column_measurements):
            dif_count = {}
            prev = chunk[0][join_column_measurements]
            for row in chunk[1::]:
                  act = row[join_column_measurements]
                  dif = self._time_difference(prev, act)
                  dif_count[dif] = dif_count.get(dif, 0) + 1
                  prev = act
            return max(dif_count, key=dif_count.get)
      
      def _apply_trans_all_to_chunk(self, chunk, join_column_measurements):
            source_columns = self._config["measurements"][self._active_measurement]["target_facts"]["source_columns"]
            source_columns_names = [sc["name"] for sc in source_columns]
            timestamp_source_column = self._config["measurements"][self._active_measurement]["target_dimensions"][1]["source_column"]
            max_approximated = self._config["max_approximated"]

            chunk = select_source_columns(chunk, source_columns_names, join_column_measurements, timestamp_source_column)
            chunk = format_timestamps(chunk, timestamp_source_column)
            chunk = sorted(chunk, key=lambda d: d[timestamp_source_column])
            
            if self._regularize_bool:
                  chunk = regularize_timestamps(chunk, join_column_measurements, timestamp_source_column, source_columns, source_columns_names)
            
            if self._correct_bool:
                  chunk = correct_measurements(chunk, source_columns, source_columns_names, timestamp_source_column, join_column_measurements, max_approximated)
            self._loader.load(chunk)

      def _apply_chosen_trans(self):
            chunk_accumulators = self._create_chunk_accumulators()
            join_column_measurements = self._config["measurements"][self._active_measurement]["target_dimensions"][0]["join_column_measurements"]
            chunk_size = self._config["chunk_size"]
            self._loader = Loader(self._config)

            while True:
                  row = self._extractor.get_next_row()
                  if not row:
                        break
                  if row[join_column_measurements] not in chunk_accumulators:
                        continue
                  chunk_accumulators[row[join_column_measurements]].append(row)

                  # when the accumulator reaches chunk_size, start transformations
                  if len(chunk_accumulators[row[join_column_measurements]]) >= chunk_size:
                        accumulator = chunk_accumulators[row[join_column_measurements]]
                        self._apply_trans_all_to_chunk(accumulator, join_column_measurements)
                        
                        # empty accumulator
                        del chunk_accumulators[row[join_column_measurements]][:]
                  
            for accumulator in chunk_accumulators.values():
                  if len(accumulator) > 0:
                        # start transformations
                        self._apply_trans_all_to_chunk(accumulator, join_column_measurements)
            
            self._extractor.close()
      
      def apply_trans_all(self):
            self._regularize_bool = True
            self._correct_bool = True
            self._apply_chosen_trans()

      def apply_trans_regularize(self):
            self._regularize_bool = True
            self._correct_bool = False
            self._apply_chosen_trans()

      def apply_trans_correct(self):
            self._regularize_bool = False
            self._correct_bool = True
            self._apply_chosen_trans()