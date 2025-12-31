def select_chosen_columns(chunk, source_columns):
    new_chunk = []

    for row in chunk:
        new_row = {}
        for column in source_columns:
            new_row[column] = row[column]
        new_chunk.append(new_row)

    return new_chunk
