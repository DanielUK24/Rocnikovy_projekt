from src.extract.CSVExtractor import CSVExtractor
from dateutil import parser
from dateinfer import infer


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
    
    def _create_middle_line(self, line1, line2):
        middle_line = {}
        for key in line1:
                # to do: genericity
                if key == "Beach Name":
                      middle_line[key] = line1[key]
                # to do: genericity
                if key == "Measurement Timestamp":
                      middle_line[key] = ""
                else:
                    if line1[key] == "" and line2[key] == "":
                          middle_line[key] = ""
                    if line1[key] != "" and line2[key] != "":
                         middle_line[key] =  round( ( float(line1[key]) + float(line2[key]) )/2 , 3 )
        return middle_line
                      
    
    def _add_missing_lines(self, lines, common_difference):
          
          # to do: implement to .json and constructor
          maximum_time_difference = 24
          
          act = lines[0]["Measurement Timestamp"]
          new_lines = [act]

          for line in lines:
            next = line["Measurement Timestamp"]
            dif = self._time_difference(act, next)

            if dif <= common_difference or maximum_time_difference < dif:
                    new_lines.append(line)
                    act = line        
                    continue

            middle_line = self._create_middle_line(act, next)
            act_time = parser.parse(act["Measurement Timestamp"])
            number_of_missing_lines = dif%common_difference

            for j in range(number_of_missing_lines):
                  middle_line["Measurement Timestamp"] = act_time + j*common_difference
                  new_lines.append(middle_line)

            new_lines.append(next)            
            prev = act

            return new_lines


    def apply_trans_all(self, lines):
         
         common_difference = self._calculate_common_difference(lines)