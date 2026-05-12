# container for input from UI
class Filter:
    def __init__(self, checked_sensors, checked_metrics, start_date, end_date):
        self.checked_sensors = checked_sensors
        self.checked_metrics = checked_metrics
        self.start_date = start_date
        self.end_date = end_date