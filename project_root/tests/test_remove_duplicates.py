import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.transform.remove_duplicates import remove_duplicates
import pandas as pd
from pandas.testing import assert_frame_equal

def test_remove_duplicates():
    chunk = [
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 08:00:00"), "Measurement 1": 1, "Measurement 2": 20},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 08:00:00"), "Measurement 1": 1, "Measurement 2": 20},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 07:00:00"), "Measurement 1": 2, "Measurement 2": 19},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 07:00:00"), "Measurement 1": 3, "Measurement 2": 18},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 07:00:00"), "Measurement 1": 4, "Measurement 2": 17},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 07:00:00"), "Measurement 1": 5, "Measurement 2": 16},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 07:00:00"), "Measurement 1": 6, "Measurement 2": 15},
    ]

    join_column_measurements = "Senzor name"
    time_source_column = "Timestamp"
    chunk_copy = chunk.copy()

    expected_output = [
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 08:00:00"), "Measurement 1": 1.0, "Measurement 2": 20.0},
        {"Senzor name": "Senzor_A", "Timestamp": pd.Timestamp("2021-08-24 07:00:00"), "Measurement 1": 4.0, "Measurement 2": 17.0},
    ]

    output = remove_duplicates(chunk_copy, join_column_measurements, time_source_column)

    df1 = pd.DataFrame(expected_output)
    df2 = pd.DataFrame(output)
    print(df1, "\n", df2)

    assert_frame_equal(df1, df2)
