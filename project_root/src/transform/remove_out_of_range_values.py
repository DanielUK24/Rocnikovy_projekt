import numpy

def remove_out_of_range_values(chunk, source_columns):
    for sc in source_columns:
        for row in chunk:
            if not sc["min_value"] < row[sc["name"]] < sc["max_value"]:
                row[sc["name"]] = numpy.nan