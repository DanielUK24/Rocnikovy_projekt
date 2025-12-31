from dateutil import parser

def format_timestamps(chunk, source_column):

    for row in chunk:
        row[source_column] = parser.parse(row[source_column])

    return chunk