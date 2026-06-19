from dateutil import parser

def format_timestamps(chunk, time_source_column):

    for row in chunk:
        row[time_source_column] = parser.parse(row[time_source_column])

    return chunk