import pandas
import numpy

def approximate(chunk, time_column, max_approximated, freq):
    data_frame = pandas.DataFrame(chunk)
    data_frame = data_frame.sort_values(time_column)
    data_frame = data_frame.set_index(time_column)

    data_frame = data_frame.asfreq(freq)

    numeric_columns = data_frame.select_dtypes(include="number").columns

    for column in numeric_columns:
        data_frame[column] = data_frame[column].interpolate(
            method = "time",
            limit = max_approximated,
            limit_area = "inside"
        )
    
    non_numeric = data_frame.select_dtypes(exclude="number").columns
    data_frame[non_numeric] = data_frame[non_numeric].ffill().bfill()
    data_frame = data_frame.sort_values(time_column, ascending = False)
    return data_frame.reset_index().to_dict("records")

def approximate_missing_values_rows(chunk, join_column_measurements, time_column, source_columns_names, max_approximated, freq):
    new_chunk = []
    buffer = [chunk[0]]

    middle_line = {}
    middle_line[join_column_measurements] = chunk[0][join_column_measurements]
    for name in source_columns_names:
        middle_line[name] = numpy.nan

    for i in range(len(chunk)-1):
        delta = abs(chunk[i][time_column] - chunk[i+1][time_column])
        delta_steps = delta / pandas.Timedelta(freq)

        if delta_steps <= max_approximated:
            buffer.append(chunk[i+1])
        else:
            # eventually add two nan lines
            after_approximation = approximate(buffer, time_column, max_approximated, freq)
            #print("AFTER APROXIMATION:\n", after_approximation)
            new_chunk.extend(after_approximation)
            middle_line[time_column] = after_approximation[-1][time_column] - pandas.Timedelta(freq)
            new_chunk.append(middle_line.copy())
            buffer = [chunk[i+1]]
    new_chunk.extend(approximate(buffer, time_column, max_approximated, freq))
    return new_chunk
