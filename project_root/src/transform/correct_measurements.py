import numpy as np
from datetime import timedelta

def correct_measurements(chunk, source_columns, source_columns_names, timestamp_source_column, sensor_source_column, max_approximated):

    common_difference = timedelta(hours = 1)

    # replace empty values and incorrect values by None
    for row in chunk:
        for column in source_columns:
            
            if row[column["name"]] == "":
                row[column["name"]] = None
                continue

            if type(row[column["name"]]) is not float:
                try:
                    row[column["name"]] = float(row[column["name"]].replace(",",""))
                except:
                    print("cannot be converted to float:", row[column["name"]])
            
            if not column["min_value"] < row[column["name"]] < column["max_value"]:
                row[column["name"]] = None

    n = len(chunk)
    last_values = {}
    for row_number in range(n):
        for column_name in source_columns_names:
            if chunk[row_number][column_name] == None:
                pass
            else:
                last_values[column_name] = chunk[row_number][column_name]

    # add missing lines
    middle_line = {}
    middle_line[sensor_source_column] = chunk[0][sensor_source_column]
    middle_line[timestamp_source_column] = None

    dividing_line = {}
    dividing_line[sensor_source_column] = chunk[0][sensor_source_column]
    dividing_line[timestamp_source_column] = None

    for column_name in source_columns_names:
        middle_line[column_name] = None
        dividing_line[column_name] = np.nan

    processed_chunk = [chunk[0]]
    prev = chunk[0]
    for row in chunk[1::]:
        act = row
        dif = act[timestamp_source_column] - prev[timestamp_source_column]
        assert dif % common_difference == timedelta(0)

        if dif/common_difference > max_approximated+1:
            new_dividing_line = dividing_line.copy()
            new_dividing_line[timestamp_source_column] = prev[timestamp_source_column] + common_difference
            processed_chunk.append(new_dividing_line)
            
        else:
            missing_rows_number = int(dif/common_difference-1)
            for i in range(1, missing_rows_number+1):
                new_middle_line = middle_line.copy()
                new_middle_line[timestamp_source_column] = prev[timestamp_source_column] + common_difference * i
                processed_chunk.append(new_middle_line)
        
        processed_chunk.append(act)
        prev = act
    
    # approximate missing values that can be approximated
    # zatial predpokladame, ze prvy riadok je plny
    for column_name in source_columns_names:
        prev_value = processed_chunk[0][column_name]
        i = 1
        while i < len(processed_chunk):

            if processed_chunk[i][column_name] == np.nan:
                pass
                # zatial neriesime
            elif processed_chunk[i][column_name] != None:
                prev = processed_chunk[i][column_name]
            else:
                j = i+1
                while j < len(processed_chunk):
                    if processed_chunk[j][column_name] != None:
                        break
                    j += 1
                
                if j == len(processed_chunk):
                    # it would be possible here to check next chunk
                    i = j
                elif j-i-1 > max_approximated:
                    i = j
                    prev = processed_chunk[i][column_name]
                else:
                    next_value = processed_chunk[j][column_name]
                    approximated_value = (prev_value+next_value)/2
                    for k in range(i,j):
                        processed_chunk[k][column_name] = approximated_value
                    i = j
                    prev = processed_chunk[i][column_name]
            
            i += 1

    return processed_chunk