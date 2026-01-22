# converts empty strings and out of range values to None
# the rest converts to float
def convert_string_measurements(chunk, source_columns):
    for row in chunk:
        for column in source_columns:
            assert isinstance(row[column["name"]], str) or isinstance(row[column["name"]], float) or row[column["name"]] == None
            
            if not isinstance(row[column["name"]], str):
                continue

            if row[column["name"]] == "":
                row[column["name"]] = None
                continue

            if type(row[column["name"]]) is not float:
                try:
                    row[column["name"]] = float(row[column["name"]].replace(",",""))
                except:
                    print("cannot be converted to float:", row[column["name"]])
            
            if not column["min_value"] <= row[column["name"]] <= column["max_value"]:
                row[column["name"]] = None
    return chunk