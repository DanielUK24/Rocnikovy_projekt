def select_source_columns(chunk, source_columns, join_column_measurements, time_source_column):
    new_chunk = []

    for row in chunk:
        new_row = {}
        new_row[join_column_measurements] = row[join_column_measurements]
        new_row[time_source_column] = row[time_source_column]
        for column in source_columns:
            new_row[column] = row[column]
        new_chunk.append(new_row)

    return new_chunk
