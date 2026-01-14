from src.extract.CSVExtractor import CSVExtractor
from src.transform.select_source_columns import select_source_columns
from src.transform.format_timestamps import format_timestamps
from src.transform.remove_duplicates import remove_duplicates
from src.transform.convert_measurement_values_to_float_or_nan import convert_measurement_values_to_float_or_nan
from src.transform.remove_out_of_range_values import remove_out_of_range_values
from src.transform.approximate_missing_values_rows import approximate_missing_values_rows
from src.transform.remove_rows_with_all_nans import remove_rows_with_all_nans
from dateutil import parser # dtd probably can be delete
import json
import pandas

class Transformer:

      def __init__(self, config_file):

           #self._chunk_size = self._config.get("chunk_size")
           #if self._chunk_size is None:
            #raise ValueError("chunk_size must be specified in config.json")
      

           self._config = self._load_config(config_file)
           self._active_measurement = self._config.get("active_measurement")
           active_measurement_path = self._config.get("measurements")[self._active_measurement].get("path")
           self._extractor = CSVExtractor(active_measurement_path)
           self._f = open("data/output/output.txt", "w", encoding="utf-8")

      
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

      def _calculate_common_difference(self, chunk, join_column_measurements):
            dif_count = {}
            prev = chunk[0][join_column_measurements]
            for row in chunk[1::]:
                  act = row[join_column_measurements]
                  dif = self._time_difference(prev, act)
                  dif_count[dif] = dif_count.get(dif, 0) + 1
                  prev = act
            print(dif_count)
            return max(dif_count, key=dif_count.get)
      
      def _apply_trans_all_to_chunk(self, chunk, join_column_measurements, time_source_column, max_approximated):
            source_columns = self._config["measurements"][self._active_measurement]["target_facts"]["source_columns"]
            source_columns_names = [sc["name"] for sc in source_columns]
            chunk = select_source_columns(chunk, source_columns_names, join_column_measurements, time_source_column)

            chunk = format_timestamps(chunk, time_source_column)
            chunk = sorted(chunk, key=lambda d: d[time_source_column], reverse=False)
            convert_measurement_values_to_float_or_nan(chunk, join_column_measurements, time_source_column)
            remove_out_of_range_values(chunk, source_columns)
            chunk = remove_duplicates(chunk, join_column_measurements, time_source_column)
            #chunk = remove_rows_with_all_nans(chunk, source_columns_names)
            # dtd edit arguments
            chunk = approximate_missing_values_rows(chunk, join_column_measurements, time_source_column, source_columns_names, max_approximated, "1h")
            
            pandas.set_option("display.max_rows", None)
            pandas.set_option("display.max_columns", None)
            pandas.set_option("display.width", None)
            data_frame = pandas.DataFrame(chunk)
            self._f.write("Transformed chunk:\n")
            self._f.write(data_frame.to_string())
            self._f.write("\n\n")


      def apply_trans_all(self):
            chunk_accumulators = self._create_chunk_accumulators()
            join_column_measurements = self._config["measurements"][self._active_measurement]["target_dimensions"][0]["join_column_measurements"]
            time_source_column = self._config["measurements"][self._active_measurement]["target_dimensions"][1]["source_column"]
            chunk_size = self._config["chunk_size"]
            max_approximated = self._config["max_approximated"]

            while True:
                  row = self._extractor.get_next_row()
                  if not row:
                        break
                  if row[join_column_measurements] not in chunk_accumulators:
                        continue
                  chunk_accumulators[row[join_column_measurements]].append(row)

                  # when an accumulator reaches chunk_size, we start transformations
                  if len(chunk_accumulators[row[join_column_measurements]]) >= chunk_size:
                        accumulator = chunk_accumulators[row[join_column_measurements]]
                        self._apply_trans_all_to_chunk(accumulator, join_column_measurements, time_source_column, max_approximated)
                        # empty accumulator
                        del chunk_accumulators[row[join_column_measurements]][:]
                  
            for accumulator in chunk_accumulators.values():
                  if len(accumulator) > 0:
                        # start transformations
                        self._apply_trans_all_to_chunk(accumulator, join_column_measurements, time_source_column, max_approximated)
            
            self._extractor.close()
            self._f.close()
