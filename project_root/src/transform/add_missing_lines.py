from dateutil import parser

def __time_difference(self, t1, t2):
    dt1 = parser.parse(t1)
    dt2 = parser.parse(t2)
    return abs(dt2 - dt1)

def __create_middle_line(self, line1, line2):
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
    maximum_time_difference = 24
    # to do: implement to .json and constructor
    
    act = lines[0]["Measurement Timestamp"]
    new_lines = [act]

    for line in lines:
        next = line["Measurement Timestamp"]
        dif = self._time_difference(act, next)
        
        if dif <= common_difference:
            new_lines.append(line)
            act = line
            continue

        if maximum_time_difference < dif:
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
