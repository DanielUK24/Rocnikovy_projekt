from src.extract.csv_extractor import CSVExtractor
from src.load.loader import Loader
from src.transform.select_source_columns import select_source_columns
from src.transform.format_timestamps import format_timestamps
from src.transform.correct_measurements import correct_measurements
from src.transform.regularize_timestamps import regularize_timestamps
from datetime import datetime

class Transformer:
      
      def __init__(self, config, active_measurement):
            
            self._config = config
            self._active_measurement = active_measurement
            active_measurement_path = self._config["measurements"][self._active_measurement]["path"]
            try:
                  self._extractor = CSVExtractor(active_measurement_path)
                  self._measurement_file_opened_succesfully = True
            except:
                  print("Measurement file with path %s not found." % (active_measurement_path))
                  self._measurement_file_opened_succesfully = False
            self._regularize_bool = False
            self._correct_bool = False
            self._loader = Loader(self._config, self._active_measurement)
      
      def _create_chunk_accumulators(self, codelist_path):
            type = self._config["measurements"][self._active_measurement]["type"]
            codelist_extractor = CSVExtractor(codelist_path)

            chunk_accumulators = {}

            while True:
                  row = codelist_extractor.get_next_row()
                  if not row:
                        break
                  if row[self._join_column_codelist] == type:
                        chunk_accumulators[row[self._sensor_name_column_codelist]] = []

            codelist_extractor.close()
            return chunk_accumulators
      
      def _get_sensor_names_from_codelist(self, codelist_path):
            codelist_extractor = CSVExtractor(codelist_path)
            sensors_from_codelist = []

            while True:
                  row = codelist_extractor.get_next_row()
                  if not row:
                        break
                  sensors_from_codelist.append(row[self._sensor_name_column_codelist])

            codelist_extractor.close()
            return sensors_from_codelist
      
      def _apply_chosen_trans_to_chunk(self, chunk, join_column_measurements, actual_sensor):

            chunk = select_source_columns(chunk, self._source_columns_names, join_column_measurements, self._timestamp_source_column)
            chunk = format_timestamps(chunk, self._timestamp_source_column)
            chunk = sorted(chunk, key=lambda d: d[self._timestamp_source_column])
            
            if self._regularize_bool:
                  chunk = regularize_timestamps(chunk, join_column_measurements, self._timestamp_source_column, self._source_columns, self._source_columns_names)
            
            if self._correct_bool:
                  chunk = correct_measurements(chunk, self._source_columns, self._source_columns_names, self._timestamp_source_column, join_column_measurements, self._max_approximated)

            measurements_to_load = []
            for row in chunk:
                  new_meas = []
                  new_meas.append(row[self._timestamp_source_column])
                  for column_name in self._source_columns_names:
                        new_meas.append(row[column_name])
                  measurements_to_load.append(new_meas)
            dates_to_load: list[datetime] = [row[self._timestamp_source_column].replace(hour=0, minute=0, second=0, microsecond=0) for row in chunk]
            self._loader.load(measurements_to_load, dates_to_load, actual_sensor)

      def _apply_chosen_trans(self):
            if not self._measurement_file_opened_succesfully:
                  print("You cannot start transformation, since measurement file did not exist.")
                  return
            
            # initial initializations
            self._source_columns = self._config["measurements"][self._active_measurement]["target_facts"]["source_columns"]
            self._source_columns_names = [sc["name"] for sc in self._source_columns]
            self._timestamp_source_column = self._config["measurements"][self._active_measurement]["source_column_for_dim_dates"]
            self._max_approximated = self._config["max_approximated"]
            self._sensor_name_column_codelist = self._config["target_dimensions"]["dim_sensors"]["sensor_name_column_codelist"]
            self._join_column_codelist = self._config["target_dimensions"]["dim_sensors"]["join_column_codelist"]

            # loading sensors from codelist to database
            codelist_path = self._config["codelist_path"]
            try:
                  sensors_from_codelist = self._get_sensor_names_from_codelist(codelist_path)
            except:
                  print("Codelist file with path %s not found." % (codelist_path))
                  return
            self._loader.load_to_dim_sensors(sensors_from_codelist)

            # creating chunk accumulators
            try:
                  chunk_accumulators = self._create_chunk_accumulators(codelist_path)
            except:
                  print("Codelist file with path %s not found." % (codelist_path))
                  return

            join_column_measurements = self._config["measurements"][self._active_measurement]["source_column_for_dim_sensors"]
            chunk_size = self._config["chunk_size"]
            
            # accumulate measurements to accumulators and transform
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
                        self._apply_chosen_trans_to_chunk(accumulator, join_column_measurements, row[join_column_measurements])
                        
                        # empty accumulator
                        del chunk_accumulators[row[join_column_measurements]][:]
                  
            for accumulator in chunk_accumulators.values():
                  if len(accumulator) > 0:
                        # start transformations
                        self._apply_chosen_trans_to_chunk(accumulator, join_column_measurements, accumulator[0][join_column_measurements])
            
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
