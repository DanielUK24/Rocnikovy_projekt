from datetime import timedelta

def create_new_row(duplicates, sensor_source_column, timestamp_source_column, source_columns_names):
    new_row = {}
    new_row[sensor_source_column] = duplicates[0][sensor_source_column]
    new_row[timestamp_source_column] = duplicates[0][timestamp_source_column]
    average_numerators = {}
    average_denominators = {}
    has_been = {}

    for column_name in source_columns_names:
        average_numerators[column_name] = 0
        average_denominators[column_name] = 0
        has_been[column_name] = False
    
    for row in duplicates:
        for column_name in source_columns_names:
            if row[column_name] != "":

                if type(row[column_name]) is not float:
                    try:
                        row[column_name] = float(row[column_name].replace(",",""))
                    except:
                        print("cannot be converted to float:", row[column_name], type(row[column_name]))
                        break
                
                average_numerators[column_name] += row[column_name]
                average_denominators[column_name] += 1
                has_been[column_name] = True
    
    for column in average_numerators:
        if has_been[column]:
            new_row[column] = average_numerators[column]/average_denominators[column]
        else:
            new_row[column] = None
    return new_row

def round_hours(dt):
    return dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours = 1 if dt.minute >= 30 else 0)

def regularize_timestamps(chunk, sensor_source_column, timestamp_source_column, source_columns_names):

    for row in chunk:
        row[timestamp_source_column] = round_hours(row[timestamp_source_column])

    new_chunk = []

    i = 0
    while i < len(chunk):

        # if the row is the last one in chunk OR the timestamp differs from the following one, then continue
        if i==len(chunk)-1 or chunk[i][timestamp_source_column] != chunk[i+1][timestamp_source_column]:
            new_chunk.append(chunk[i])
            i += 1
            continue

        duplicates = [chunk[i]]
        j = i+1

        while j < len(chunk) and chunk[j][timestamp_source_column] == chunk[i][timestamp_source_column]:
            duplicates.append(chunk[j])
            j += 1
        
        new_row = create_new_row(duplicates, sensor_source_column, timestamp_source_column, source_columns_names)
        new_chunk.append(new_row)

        i = j
   
    return new_chunk
