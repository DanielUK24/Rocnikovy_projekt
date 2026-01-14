import numpy

def remove_rows_with_all_nans(chunk, source_columns_names):
    new_chunk = []
    not_all_nans = False
    for row in chunk:
        for column in source_columns_names:
            if not numpy.isnan(row[column]):
                not_all_nans = True
        if not_all_nans:
            new_chunk.append(row)
            not_all_nans = False
    return new_chunk