import numpy as np
from datetime import timedelta
from src.transform.convert_string_measurements import convert_string_measurements

TIME_BREAK = object()

# returns the value of nearest float from index i in chunk according to direction
# and number of missing rows between them
def find_nearest_float(chunk, i, column, direction):
    assert direction == "forward" or direction == "backward"
    if direction == "forward": d = 1
    else: d = -1

    j = i + d
    missing = 0
    while 0 <= j < len(chunk):
        assert type(chunk[j][column]) == float or chunk[j][column] == None or chunk[j][column] == TIME_BREAK
        if type(chunk[j][column]) == float:
            return (chunk[j][column],missing)
        if chunk[j][column] == TIME_BREAK:
            return (None, missing)
        missing += 1
        j = j + d
    
    return (None, missing)

def fill_range_by_value(chunk, column, start, end, value):
    j = start
    while start <= j <= end:
        chunk[j][column] = value
        j += 1

def calculate_approximated_value(value1, value2):
    assert type(value1) == float or type(value2) == float
    assert value1 != None or value2 != None
    assert value1 != TIME_BREAK and value2 != TIME_BREAK
    if value1 != None and value2 != None:
        return (value1+value2)/2
    elif value1 != None:
        return value1
    else:
        return value2

def correct_measurements(chunk, source_columns, source_columns_names, timestamp_source_column, sensor_source_column, max_approximated):

    common_difference = timedelta(hours = 1)

    chunk = convert_string_measurements(chunk, source_columns)
    
    # add missing rows
    middle_row = {}
    middle_row[sensor_source_column] = chunk[0][sensor_source_column]
    middle_row[timestamp_source_column] = None

    dividing_row = {}
    dividing_row[sensor_source_column] = chunk[0][sensor_source_column]
    dividing_row[timestamp_source_column] = None

    for column_name in source_columns_names:
        middle_row[column_name] = None
        dividing_row[column_name] = TIME_BREAK
    
    chunk_rows_added = [chunk[0]]
    prev = chunk[0]
    for row in chunk[1::]:
        act = row
        dif = abs(act[timestamp_source_column] - prev[timestamp_source_column])
        assert dif % common_difference == timedelta(0)

        if dif/common_difference > max_approximated+1:
            new_dividing_row = dividing_row.copy()
            new_dividing_row[timestamp_source_column] = prev[timestamp_source_column] + common_difference
            chunk_rows_added.append(new_dividing_row)
            
        else:
            missing_rows_number = int(dif/common_difference-1)
            for i in range(1, missing_rows_number+1):
                new_middle_row = middle_row.copy()
                new_middle_row[timestamp_source_column] = prev[timestamp_source_column] + common_difference * i
                chunk_rows_added.append(new_middle_row)
        
        chunk_rows_added.append(act)
        prev = act

    # approximate missing values that can be approximated
    for column_name in source_columns_names:

        i = -1
        previous = None
        while i < len(chunk_rows_added):

            if i == -1 or chunk_rows_added[i][column_name] == TIME_BREAK:
                nfloat_missing = find_nearest_float(chunk_rows_added, i, column_name, "forward")
                nfloat = nfloat_missing[0]
                missing = nfloat_missing[1]

                if nfloat == None:
                    break
                assert type(nfloat) == float
                assert missing >= 0
                if missing == 0:
                    previous = nfloat
                    i = i+1
                else:
                    nfloat_missing_2 = find_nearest_float(chunk_rows_added, i, column_name, "backward")
                    nfloat_2 = nfloat_missing_2[0]
                    missing_2 = nfloat_missing_2[1]
                    assert missing_2 >= 0
                    if missing > max_approximated:
                        previous = nfloat
                        i = i+1
                    else:
                        start = i+1
                        end = i+missing
                        approx = calculate_approximated_value(nfloat, nfloat_2)
                        fill_range_by_value(chunk_rows_added, column_name, start, end, approx)
                        previous = nfloat
                        i = i+1
            elif type(chunk_rows_added[i][column_name]) == float:
                previous = chunk_rows_added[i][column_name]
            else:
                assert chunk_rows_added[i][column_name] == None
                assert type(previous) == float
                nfloat_missing = find_nearest_float(chunk_rows_added, i, column_name, "forward")
                nfloat = nfloat_missing[0]
                missing = nfloat_missing[1]
                assert missing >= 0
                if missing+1 <= max_approximated:
                    following = nfloat
                    start = i
                    end = i+missing
                    approx = calculate_approximated_value(previous, following)
                    fill_range_by_value(chunk_rows_added, column_name, start, end, approx)
                    previous = following
                    i = i+missing
                else:
                    previous = nfloat
                    i = i+missing
            
            i += 1

    for row in chunk_rows_added:
        for column_name in source_columns_names:
            if row[column_name] == TIME_BREAK:
                row[column_name] = np.nan
    
    return chunk_rows_added