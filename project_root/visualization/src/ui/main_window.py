import os
import numpy as np
from datetime import datetime, timedelta

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QScrollArea, QCheckBox, QGridLayout, QPushButton, QComboBox, QGroupBox, QLayout
from PySide6.QtCore import Qt, QDate

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from src.meta_data_reader import MetaDataReader
from src.query_service import QueryService

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta_data_reader = MetaDataReader()
        self._query_service = QueryService()
        self._current_fact_table = None
        self.setWindowTitle('Visualizator')
        self.resize(1000,500)
        self._build_ui()

    def show(self): 
        self._fact_selection.clear()
        self._fact_selection.addItems(self._meta_data_reader.get_fct_tables())
        self._clearLayout(self._sensor_layout)
        self._clearLayout(self._metric_layout)
        super().show()

    def set_conn_window(self, conn_window):
        self._conn_window = conn_window

    def _build_ui(self):

        control_graph_container = QWidget()
        self.setCentralWidget(control_graph_container)
        container_layout = QHBoxLayout()
        control_graph_container.setLayout(container_layout)

        control_panel = QWidget()
        container_layout.addWidget(control_panel)

        control_layout = QVBoxLayout()
        control_panel.setLayout(control_layout)

        # set connection button
        connection_button = QPushButton('<< Set connection')
        connection_button.clicked.connect(self._on_set_clicked)
        control_layout.addWidget(connection_button)

        # groupbox
        fct_table_selection = QGroupBox("Fact table selection")
        fct_table_selection_layout = QVBoxLayout()
        fct_table_selection.setLayout(fct_table_selection_layout)
        control_layout.addWidget(fct_table_selection)

        # fact table selection label
        fact_label = QLabel('Select fact table')
        fact_label.setAlignment(Qt.AlignLeft)
        fct_table_selection_layout.addWidget(fact_label)

        # fact table selection
        self._fact_selection = QComboBox()
        fct_table_selection_layout.addWidget(self._fact_selection)

        # show button
        show_button = QPushButton('Show')
        show_button.clicked.connect(self._on_show_clicked)
        fct_table_selection_layout.addWidget(show_button)

        # plot configuration groupbox
        configuration = QGroupBox("Plot configuration")
        control_layout.addWidget(configuration)
        configuration_layout = QGridLayout()
        configuration.setLayout(configuration_layout)

        # start_datetime date label
        start_label = QLabel('Start date')
        start_label.setAlignment(Qt.AlignLeft)
        configuration_layout.addWidget(start_label,8,0)

        # start_datetime date selection
        self._start_date = QDateEdit()
        self._start_date.setCalendarPopup(True)
        self._start_date.setDate(QDate(2014,6,1))
        configuration_layout.addWidget(self._start_date,10,0)

        # end_datetime date label
        end_label = QLabel('End date')
        end_label.setAlignment(Qt.AlignLeft)
        configuration_layout.addWidget(end_label,8,1)

        # end_datetime date selection
        self._end_date = QDateEdit()
        self._end_date.setCalendarPopup(True)
        self._end_date.setDate(QDate(2014,6,10))
        configuration_layout.addWidget(self._end_date,10,1)

        # sensor and metric selection label
        sensor_metric_label = QLabel("Select")
        sensor_metric_label.setAlignment(Qt.AlignLeft)
        sensor_metric_label.setToolTip('''
            Choose items so that one list has exactly one selection 
            while the other has one or more selections.
            You may choose which list has the single selection.
        ''')
        configuration_layout.addWidget(sensor_metric_label,15,0)

        # sensor selection
        sensor_scroll = QScrollArea()
        sensor_scroll.setWidgetResizable(True)

        sensor_container = QWidget()
        self._sensor_layout = QVBoxLayout(sensor_container)
        self._sensor_layout.setAlignment(Qt.AlignTop)
        self._sensor_layout.addStretch()
        
        sensor_scroll.setWidget(sensor_container)
        
        configuration_layout.addWidget(sensor_scroll,20,0)

        # metric selection
        metric_scroll = QScrollArea()
        metric_scroll.setWidgetResizable(True)

        metric_container = QWidget()
        self._metric_layout = QVBoxLayout(metric_container)
        self._metric_layout.setAlignment(Qt.AlignTop)
        self._metric_layout.addStretch()
        
        metric_scroll.setWidget(metric_container)
        
        configuration_layout.addWidget(metric_scroll,20,1)

        # load button
        load_button = QPushButton('Load')
        load_button.clicked.connect(self._on_load_clicked)
        configuration_layout.addWidget(load_button,30,0)

        # graph part
        self._sc = MplCanvas(self, width=5, height=4, dpi=100)
        container_layout.addWidget(self._sc)

    def _on_show_clicked(self):
        self._current_fact_table = self._fact_selection.currentText()
        sensors = self._meta_data_reader.get_sensors(self._current_fact_table)
        metrics = self._meta_data_reader.get_metrics(self._current_fact_table)

        self._metric_checkboxes = []
        self._sensor_checkboxes = []

        self._clearLayout(self._sensor_layout)
        self._clearLayout(self._metric_layout)

        for sensor in sensors:
            cb = QCheckBox(sensor)
            self._sensor_checkboxes.append(cb)
            self._sensor_layout.addWidget(cb)

        for metric in metrics:
            cb = QCheckBox(metric)
            self._metric_checkboxes.append(cb)
            self._metric_layout.addWidget(cb)

    def _on_load_clicked(self):

        if self._current_fact_table == None:
            raise Exception("Fact table not chosen")

        start_date = self._start_date.date().toPython()
        end_date = self._end_date.date().toPython()

        start_datetime = datetime(start_date.year, start_date.month, start_date.day)
        end_datetime = datetime(end_date.year, end_date.month, end_date.day)

        if start_datetime > end_datetime:
            raise Exception("Start date after end date")

        chosen_sensors = []
        chosen_metrics = []

        for cb in self._sensor_checkboxes:
            if cb.isChecked():
                chosen_sensors.append(cb.text())
        
        for cb in self._metric_checkboxes:
            if cb.isChecked():
                chosen_metrics.append(cb.text())

        if len(chosen_sensors) == 0 or len(chosen_metrics) == 0:
            # iba zmena osi x
            return
        
        # one sensor, many metrics
        elif len(chosen_sensors) == 1 and len(chosen_metrics) > 0:    

            timestamp_measurements = self._query_service.get_data_one_sensor_many_metrics(self._current_fact_table, chosen_sensors[0], chosen_metrics, start_datetime, end_datetime)

            # creating list for x axis
            # creating list for y axis
            i = 0
            x = []
            chosen_metrics_len = len(chosen_metrics)
            y = [[] for _ in range(chosen_metrics_len)]
            current_datetime = start_datetime
            while current_datetime < end_datetime + timedelta(days=1):
                
                x.append(current_datetime)
                
                if i < len(timestamp_measurements) and timestamp_measurements[i][0] == current_datetime:
                    for j in range(1, chosen_metrics_len+1):
                        y[j].append(timestamp_measurements[i][j])
                    i += 1
                else:
                    for j in range(chosen_metrics_len):
                        y[j].append(np.nan)
                current_datetime += timedelta(hours=1)

        # one metric, many sensors
        elif len(chosen_sensors) > 0 and len(chosen_metrics) == 1:

            metric_values_for_sensors = self._query_service.get_data_many_sensors_one_metric(self._current_fact_table, chosen_sensors, chosen_metrics[0], start_datetime, end_datetime)

            x = []
            current_datetime = start_datetime
            while current_datetime <= end_datetime + timedelta(days=1):
                x.append(current_datetime)
                current_datetime += timedelta(hours=1)

            indices = [0 for _ in range(len(chosen_sensors))]
            y = [[] for _ in range(len(chosen_sensors))]
            for time in x:
                for i in range(len(chosen_sensors)):
                    if indices[i] < len(metric_values_for_sensors[i]) and metric_values_for_sensors[i][indices[i]][0] == time:
                        y[i].append(metric_values_for_sensors[i][indices[i]][1])
                        indices[i] += 1
                    else:
                        y[i].append(np.nan)

            for i in range(len(chosen_sensors)):
                self._sc.plot(x, y[i], label=chosen_sensors[i])
            self._sc.plot.set_xlabel('Time')
            self._sc.plot.set_ylabel(chosen_metrics[0])

        else:
            # many to many vynimka
            pass
    

    def _on_set_clicked(self):
        self._conn_window.show()

    def _clearLayout(self, layout):
        if isinstance(layout, QLayout):
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self._clearLayout(item.layout())