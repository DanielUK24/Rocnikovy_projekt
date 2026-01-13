import pandas

def remove_duplicates(chunk, join_column_measurements, time_source_column):
    data_frame = pandas.DataFrame(chunk)
    numeric_columns = data_frame.select_dtypes(include="number").columns

    result = (
        data_frame
        .groupby([join_column_measurements, time_source_column], as_index=False)
        .agg({column: "mean" for column in numeric_columns})
    )

    return result.to_dict("records")
