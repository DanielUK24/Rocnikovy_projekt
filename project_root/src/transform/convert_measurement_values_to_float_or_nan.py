import numpy

# does not return new chunk, just edit chunk given as the argument
def convert_measurement_values_to_float_or_nan(chunk, join_column_measurements, time_source_column):
    for row in chunk:
        for attribute in row:
            if attribute == join_column_measurements or attribute == time_source_column:
                continue
            if row[attribute] == '':
                row[attribute] = numpy.nan
                continue
            try:
                row[attribute] = float(row[attribute].replace(",",""))
            except:
                # dtd throw an exception
                print("cannot be converted:", row[attribute])
                pass

            