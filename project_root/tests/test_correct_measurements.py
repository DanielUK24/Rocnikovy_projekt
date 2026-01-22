import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.transform.correct_measurements import correct_measurements
import datetime

source_columns = [
        {
        "name":"Water Temperature",
        "min_value": -5,
        "max_value": 40
        },
        {  
        "name": "Turbidity",
        "min_value": 0,
        "max_value": 1000
        },
        {  
        "name": "Transducer Depth",
        "min_value": 0,
        "max_value": 50
        },
        {  
        "name": "Wave Height",
        "min_value": 0,
        "max_value": 20
        },
        {  
        "name": "Wave Period",
        "min_value": 0,
        "max_value": 30
        },
        {  
        "name": "Battery Life",
        "min_value": 0,
        "max_value": 15
        }
    ]

source_columns_names = ["Water Temperature","Turbidity","Transducer Depth","Wave Height","Wave Period","Battery Life"]

def test01():
    given_input = [
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 12, 0), 'Water Temperature': '25', 'Turbidity': '0.82', 'Transducer Depth': '1', 'Wave Height': '0.122', 'Wave Period': '4', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 11, 0), 'Water Temperature': '23.8', 'Turbidity': '0.76', 'Transducer Depth': '1', 'Wave Height': '0.179', 'Wave Period': '3', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 10, 0), 'Water Temperature': '23.9', 'Turbidity': '0.74', 'Transducer Depth': '1', 'Wave Height': '0.099', 'Wave Period': '3', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 9, 0), 'Water Temperature': '23.2', 'Turbidity': '0.81', 'Transducer Depth': '1', 'Wave Height': '0.094', 'Wave Period': '5', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 8, 0), 'Water Temperature': '22.9', 'Turbidity': '0.97', 'Transducer Depth': '1', 'Wave Height': '0.07', 'Wave Period': '6', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 7, 0), 'Water Temperature': '22.8', 'Turbidity': '0.92', 'Transducer Depth': '1', 'Wave Height': '0.103', 'Wave Period': '7', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 6, 0), 'Water Temperature': '22.8', 'Turbidity': '1.19', 'Transducer Depth': '1', 'Wave Height': '0.08', 'Wave Period': '8', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 5, 0), 'Water Temperature': '22.8', 'Turbidity': '0.87', 'Transducer Depth': '1', 'Wave Height': '0.074', 'Wave Period': '4', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 4, 0), 'Water Temperature': '22.8', 'Turbidity': '0.87', 'Transducer Depth': '1', 'Wave Height': '0.079', 'Wave Period': '5', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 3, 0), 'Water Temperature': '22.9', 'Turbidity': '0.94', 'Transducer Depth': '1', 'Wave Height': '0.078', 'Wave Period': '5', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 2, 0), 'Water Temperature': '22.9', 'Turbidity': '0.76', 'Transducer Depth': '1', 'Wave Height': '0.086', 'Wave Period': '7', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 1, 0), 'Water Temperature': '22.9', 'Turbidity': '0.86', 'Transducer Depth': '1', 'Wave Height': '0.084', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 0, 0), 'Water Temperature': '23', 'Turbidity': '0.73', 'Transducer Depth': '1', 'Wave Height': '0.093', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 23, 0), 'Water Temperature': '23', 'Turbidity': '0.82', 'Transducer Depth': '1', 'Wave Height': '0.102', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 22, 0), 'Water Temperature': '23.1', 'Turbidity': '0.75', 'Transducer Depth': '1', 'Wave Height': '0.121', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 21, 0), 'Water Temperature': '23.1', 'Turbidity': '0.87', 'Transducer Depth': '1', 'Wave Height': '0.151', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 20, 0), 'Water Temperature': '23.1', 'Turbidity': '1.09', 'Transducer Depth': '1', 'Wave Height': '0.154', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 19, 0), 'Water Temperature': '23.2', 'Turbidity': '1.17', 'Transducer Depth': '1', 'Wave Height': '0.194', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 18, 0), 'Water Temperature': '23.3', 'Turbidity': '1.28', 'Transducer Depth': '1', 'Wave Height': '0.165', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 17, 0), 'Water Temperature': '23.2', 'Turbidity': '1.31', 'Transducer Depth': '1', 'Wave Height': '0.174', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 16, 0), 'Water Temperature': '23.2', 'Turbidity': '1.43', 'Transducer Depth': '1', 'Wave Height': '0.176', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 15, 0), 'Water Temperature': '23.3', 'Turbidity': '1.65', 'Transducer Depth': '1', 'Wave Height': '0.168', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 14, 0), 'Water Temperature': '23.1', 'Turbidity': '1.7', 'Transducer Depth': '1', 'Wave Height': '0.214', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 13, 0), 'Water Temperature': '23.3', 'Turbidity': '1.61', 'Transducer Depth': '1', 'Wave Height': '0.184', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 12, 0), 'Water Temperature': '22.7', 'Turbidity': '1.54', 'Transducer Depth': '1', 'Wave Height': '0.196', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 11, 0), 'Water Temperature': '22.1', 'Turbidity': '1.98', 'Transducer Depth': '1', 'Wave Height': '0.184', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 10, 0), 'Water Temperature': '22', 'Turbidity': '1.75', 'Transducer Depth': '1', 'Wave Height': '0.19', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 9, 0), 'Water Temperature': '21.8', 'Turbidity': '1.74', 'Transducer Depth': '1', 'Wave Height': '0.209', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 8, 0), 'Water Temperature': '21.6', 'Turbidity': '1.58', 'Transducer Depth': '1', 'Wave Height': '0.211', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 7, 0), 'Water Temperature': '21.5', 'Turbidity': '1.66', 'Transducer Depth': '1', 'Wave Height': '0.237', 'Wave Period': '6', 'Battery Life': '11.4'}]
    expected_output = [
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 12, 0), 'Water Temperature': 25.0, 'Turbidity': 0.82, 'Transducer Depth': 1.0, 'Wave Height': 0.122, 'Wave Period': 4.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 11, 0), 'Water Temperature': 23.8, 'Turbidity': 0.76, 'Transducer Depth': 1.0, 'Wave Height': 0.179, 'Wave Period': 3.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 10, 0), 'Water Temperature': 23.9, 'Turbidity': 0.74, 'Transducer Depth': 1.0, 'Wave Height': 0.099, 'Wave Period': 3.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 9, 0), 'Water Temperature': 23.2, 'Turbidity': 0.81, 'Transducer Depth': 1.0, 'Wave Height': 0.094, 'Wave Period': 5.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 8, 0), 'Water Temperature': 22.9, 'Turbidity': 0.97, 'Transducer Depth': 1.0, 'Wave Height': 0.07, 'Wave Period': 6.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 7, 0), 'Water Temperature': 22.8, 'Turbidity': 0.92, 'Transducer Depth': 1.0, 'Wave Height': 0.103, 'Wave Period': 7.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 6, 0), 'Water Temperature': 22.8, 'Turbidity': 1.19, 'Transducer Depth': 1.0, 'Wave Height': 0.08, 'Wave Period': 8.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 5, 0), 'Water Temperature': 22.8, 'Turbidity': 0.87, 'Transducer Depth': 1.0, 'Wave Height': 0.074, 'Wave Period': 4.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 4, 0), 'Water Temperature': 22.8, 'Turbidity': 0.87, 'Transducer Depth': 1.0, 'Wave Height': 0.079, 'Wave Period': 5.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 3, 0), 'Water Temperature': 22.9, 'Turbidity': 0.94, 'Transducer Depth': 1.0, 'Wave Height': 0.078, 'Wave Period': 5.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 2, 0), 'Water Temperature': 22.9, 'Turbidity': 0.76, 'Transducer Depth': 1.0, 'Wave Height': 0.086, 'Wave Period': 7.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 1, 0), 'Water Temperature': 22.9, 'Turbidity': 0.86, 'Transducer Depth': 1.0, 'Wave Height': 0.084, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 0, 0), 'Water Temperature': 23.0, 'Turbidity': 0.73, 'Transducer Depth': 1.0, 'Wave Height': 0.093, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 23, 0), 'Water Temperature': 23.0, 'Turbidity': 0.82, 'Transducer Depth': 1.0, 'Wave Height': 0.102, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 22, 0), 'Water Temperature': 23.1, 'Turbidity': 0.75, 'Transducer Depth': 1.0, 'Wave Height': 0.121, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 21, 0), 'Water Temperature': 23.1, 'Turbidity': 0.87, 'Transducer Depth': 1.0, 'Wave Height': 0.151, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 20, 0), 'Water Temperature': 23.1, 'Turbidity': 1.09, 'Transducer Depth': 1.0, 'Wave Height': 0.154, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 19, 0), 'Water Temperature': 23.2, 'Turbidity': 1.17, 'Transducer Depth': 1.0, 'Wave Height': 0.194, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 18, 0), 'Water Temperature': 23.3, 'Turbidity': 1.28, 'Transducer Depth': 1.0, 'Wave Height': 0.165, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 17, 0), 'Water Temperature': 23.2, 'Turbidity': 1.31, 'Transducer Depth': 1.0, 'Wave Height': 0.174, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 16, 0), 'Water Temperature': 23.2, 'Turbidity': 1.43, 'Transducer Depth': 1.0, 'Wave Height': 0.176, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 15, 0), 'Water Temperature': 23.3, 'Turbidity': 1.65, 'Transducer Depth': 1.0, 'Wave Height': 0.168, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 14, 0), 'Water Temperature': 23.1, 'Turbidity': 1.7, 'Transducer Depth': 1.0, 'Wave Height': 0.214, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 13, 0), 'Water Temperature': 23.3, 'Turbidity': 1.61, 'Transducer Depth': 1.0, 'Wave Height': 0.184, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 12, 0), 'Water Temperature': 22.7, 'Turbidity': 1.54, 'Transducer Depth': 1.0, 'Wave Height': 0.196, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 11, 0), 'Water Temperature': 22.1, 'Turbidity': 1.98, 'Transducer Depth': 1.0, 'Wave Height': 0.184, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 10, 0), 'Water Temperature': 22.0, 'Turbidity': 1.75, 'Transducer Depth': 1.0, 'Wave Height': 0.19, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 9, 0), 'Water Temperature': 21.8, 'Turbidity': 1.74, 'Transducer Depth': 1.0, 'Wave Height': 0.209, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 8, 0), 'Water Temperature': 21.6, 'Turbidity': 1.58, 'Transducer Depth': 1.0, 'Wave Height': 0.211, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 7, 0), 'Water Temperature': 21.5, 'Turbidity': 1.66, 'Transducer Depth': 1.0, 'Wave Height': 0.237, 'Wave Period': 6.0, 'Battery Life': 11.4}]

    function_output = correct_measurements(given_input, source_columns, source_columns_names, "Measurement Timestamp", "Beach Name", 5)

    for i in range(len(expected_output)):
        assert expected_output[i] == function_output[i]
    
def test02():
    given_input = [
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 12, 0), 'Water Temperature': '25', 'Turbidity': '0.82', 'Transducer Depth': '1', 'Wave Height': '0.122', 'Wave Period': '4', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 11, 0), 'Water Temperature': '23.8', 'Turbidity': '0.76', 'Transducer Depth': '1', 'Wave Height': '0.179', 'Wave Period': '3', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 10, 0), 'Water Temperature': '', 'Turbidity': '0.74', 'Transducer Depth': '1', 'Wave Height': '0.099', 'Wave Period': '3', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 9, 0), 'Water Temperature': '', 'Turbidity': '0.81', 'Transducer Depth': '1', 'Wave Height': '0.094', 'Wave Period': '5', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 8, 0), 'Water Temperature': '22.9', 'Turbidity': '0.97', 'Transducer Depth': '1', 'Wave Height': '0.07', 'Wave Period': '6', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 7, 0), 'Water Temperature': '22.8', 'Turbidity': '0.92', 'Transducer Depth': '1', 'Wave Height': '0.103', 'Wave Period': '7', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 6, 0), 'Water Temperature': '', 'Turbidity': '1.19', 'Transducer Depth': '1', 'Wave Height': '0.08', 'Wave Period': '8', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 5, 0), 'Water Temperature': '', 'Turbidity': '0.87', 'Transducer Depth': '1', 'Wave Height': '0.074', 'Wave Period': '4', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 4, 0), 'Water Temperature': '22.8', 'Turbidity': '0.87', 'Transducer Depth': '1', 'Wave Height': '0.079', 'Wave Period': '5', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 3, 0), 'Water Temperature': '22.9', 'Turbidity': '0.94', 'Transducer Depth': '1', 'Wave Height': '0.078', 'Wave Period': '5', 'Battery Life': '11.3'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 2, 0), 'Water Temperature': '22.9', 'Turbidity': '0.76', 'Transducer Depth': '1', 'Wave Height': '0.086', 'Wave Period': '7', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 1, 0), 'Water Temperature': '22.9', 'Turbidity': '0.86', 'Transducer Depth': '1', 'Wave Height': '0.084', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 0, 0), 'Water Temperature': '23', 'Turbidity': '0.73', 'Transducer Depth': '1', 'Wave Height': '0.093', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 23, 0), 'Water Temperature': '23', 'Turbidity': '0.82', 'Transducer Depth': '1', 'Wave Height': '0.102', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 22, 0), 'Water Temperature': '23.1', 'Turbidity': '0.75', 'Transducer Depth': '1', 'Wave Height': '0.121', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 21, 0), 'Water Temperature': '', 'Turbidity': '0.87', 'Transducer Depth': '1', 'Wave Height': '0.151', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 20, 0), 'Water Temperature': '', 'Turbidity': '1.09', 'Transducer Depth': '1', 'Wave Height': '0.154', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 19, 0), 'Water Temperature': '', 'Turbidity': '1.17', 'Transducer Depth': '1', 'Wave Height': '0.194', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 18, 0), 'Water Temperature': '', 'Turbidity': '1.28', 'Transducer Depth': '1', 'Wave Height': '0.165', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 17, 0), 'Water Temperature': '', 'Turbidity': '1.31', 'Transducer Depth': '1', 'Wave Height': '0.174', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 16, 0), 'Water Temperature': '23.2', 'Turbidity': '1.43', 'Transducer Depth': '1', 'Wave Height': '0.176', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 15, 0), 'Water Temperature': '', 'Turbidity': '1.65', 'Transducer Depth': '1', 'Wave Height': '0.168', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 14, 0), 'Water Temperature': '', 'Turbidity': '1.7', 'Transducer Depth': '1', 'Wave Height': '0.214', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 13, 0), 'Water Temperature': '', 'Turbidity': '1.61', 'Transducer Depth': '1', 'Wave Height': '0.184', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 12, 0), 'Water Temperature': '', 'Turbidity': '1.54', 'Transducer Depth': '1', 'Wave Height': '0.196', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 11, 0), 'Water Temperature': '', 'Turbidity': '1.98', 'Transducer Depth': '1', 'Wave Height': '0.184', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 10, 0), 'Water Temperature': '', 'Turbidity': '1.75', 'Transducer Depth': '1', 'Wave Height': '0.19', 'Wave Period': '5', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 9, 0), 'Water Temperature': '21.8', 'Turbidity': '1.74', 'Transducer Depth': '1', 'Wave Height': '0.209', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 8, 0), 'Water Temperature': '21.6', 'Turbidity': '1.58', 'Transducer Depth': '1', 'Wave Height': '0.211', 'Wave Period': '4', 'Battery Life': '11.4'},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 7, 0), 'Water Temperature': '21.5', 'Turbidity': '1.66', 'Transducer Depth': '1', 'Wave Height': '0.237', 'Wave Period': '6', 'Battery Life': '11.4'}
        ]
    expected_output = [
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 12, 0), 'Water Temperature': 25.0, 'Turbidity': 0.82, 'Transducer Depth': 1.0, 'Wave Height': 0.122, 'Wave Period': 4.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 11, 0), 'Water Temperature': 23.8, 'Turbidity': 0.76, 'Transducer Depth': 1.0, 'Wave Height': 0.179, 'Wave Period': 3.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 10, 0), 'Water Temperature': 23.35, 'Turbidity': 0.74, 'Transducer Depth': 1.0, 'Wave Height': 0.099, 'Wave Period': 3.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 9, 0), 'Water Temperature': 23.35, 'Turbidity': 0.81, 'Transducer Depth': 1.0, 'Wave Height': 0.094, 'Wave Period': 5.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 8, 0), 'Water Temperature': 22.9, 'Turbidity': 0.97, 'Transducer Depth': 1.0, 'Wave Height': 0.07, 'Wave Period': 6.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 7, 0), 'Water Temperature': 22.8, 'Turbidity': 0.92, 'Transducer Depth': 1.0, 'Wave Height': 0.103, 'Wave Period': 7.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 6, 0), 'Water Temperature': 22.8, 'Turbidity': 1.19, 'Transducer Depth': 1.0, 'Wave Height': 0.08, 'Wave Period': 8.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 5, 0), 'Water Temperature': 22.8, 'Turbidity': 0.87, 'Transducer Depth': 1.0, 'Wave Height': 0.074, 'Wave Period': 4.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 4, 0), 'Water Temperature': 22.8, 'Turbidity': 0.87, 'Transducer Depth': 1.0, 'Wave Height': 0.079, 'Wave Period': 5.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 3, 0), 'Water Temperature': 22.9, 'Turbidity': 0.94, 'Transducer Depth': 1.0, 'Wave Height': 0.078, 'Wave Period': 5.0, 'Battery Life': 11.3},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 2, 0), 'Water Temperature': 22.9, 'Turbidity': 0.76, 'Transducer Depth': 1.0, 'Wave Height': 0.086, 'Wave Period': 7.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 1, 0), 'Water Temperature': 22.9, 'Turbidity': 0.86, 'Transducer Depth': 1.0, 'Wave Height': 0.084, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 24, 0, 0), 'Water Temperature': 23.0, 'Turbidity': 0.73, 'Transducer Depth': 1.0, 'Wave Height': 0.093, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 23, 0), 'Water Temperature': 23.0, 'Turbidity': 0.82, 'Transducer Depth': 1.0, 'Wave Height': 0.102, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 22, 0), 'Water Temperature': 23.1, 'Turbidity': 0.75, 'Transducer Depth': 1.0, 'Wave Height': 0.121, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 21, 0), 'Water Temperature': 23.15, 'Turbidity': 0.87, 'Transducer Depth': 1.0, 'Wave Height': 0.151, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 20, 0), 'Water Temperature': 23.15, 'Turbidity': 1.09, 'Transducer Depth': 1.0, 'Wave Height': 0.154, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 19, 0), 'Water Temperature': 23.15, 'Turbidity': 1.17, 'Transducer Depth': 1.0, 'Wave Height': 0.194, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 18, 0), 'Water Temperature': 23.15, 'Turbidity': 1.28, 'Transducer Depth': 1.0, 'Wave Height': 0.165, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 17, 0), 'Water Temperature': 23.15, 'Turbidity': 1.31, 'Transducer Depth': 1.0, 'Wave Height': 0.174, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 16, 0), 'Water Temperature': 23.2, 'Turbidity': 1.43, 'Transducer Depth': 1.0, 'Wave Height': 0.176, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 15, 0), 'Water Temperature': None, 'Turbidity': 1.65, 'Transducer Depth': 1.0, 'Wave Height': 0.168, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 14, 0), 'Water Temperature': None, 'Turbidity': 1.7, 'Transducer Depth': 1.0, 'Wave Height': 0.214, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 13, 0), 'Water Temperature': None, 'Turbidity': 1.61, 'Transducer Depth': 1.0, 'Wave Height': 0.184, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 12, 0), 'Water Temperature': None, 'Turbidity': 1.54, 'Transducer Depth': 1.0, 'Wave Height': 0.196, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 11, 0), 'Water Temperature': None, 'Turbidity': 1.98, 'Transducer Depth': 1.0, 'Wave Height': 0.184, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 10, 0), 'Water Temperature': None, 'Turbidity': 1.75, 'Transducer Depth': 1.0, 'Wave Height': 0.19, 'Wave Period': 5.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 9, 0), 'Water Temperature': 21.8, 'Turbidity': 1.74, 'Transducer Depth': 1.0, 'Wave Height': 0.209, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 8, 0), 'Water Temperature': 21.6, 'Turbidity': 1.58, 'Transducer Depth': 1.0, 'Wave Height': 0.211, 'Wave Period': 4.0, 'Battery Life': 11.4},
        {'Beach Name': 'Ohio Street Beach', 'Measurement Timestamp': datetime.datetime(2021, 8, 23, 7, 0), 'Water Temperature': 21.5, 'Turbidity': 1.66, 'Transducer Depth': 1.0, 'Wave Height': 0.237, 'Wave Period': 6.0, 'Battery Life': 11.4}]

    function_output = correct_measurements(given_input, source_columns, source_columns_names, "Measurement Timestamp", "Beach Name", 5)

    for i in range(len(expected_output)):
        assert expected_output[i] == function_output[i]