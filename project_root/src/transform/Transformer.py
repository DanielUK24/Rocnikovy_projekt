from src.extract.CSVExtractor import CSVExtractor
from dateutil import parser

class Trasformer:
    def __init__(self, csv_file_path):

        # to do: do we want to add also option for parameter config_file_path ?
        self._extractor = CSVExtractor(csv_file_path)
        # to do: extractor.close()

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

    def apply_trans_all(self, lines):
         
         common_difference = self._calculate_common_difference(lines)