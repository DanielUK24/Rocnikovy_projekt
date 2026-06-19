import os
import psycopg
import numpy as np
from datetime import datetime, timedelta

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QScrollArea, QCheckBox, QGridLayout, QPushButton, QComboBox, QGroupBox, QLayout, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QCloseEvent

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from src.db_conn_manager import DBConnectionManager
from src.meta_data_reader import MetaDataReader
from src.query_service import QueryService

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class CustomDialog(QDialog):
    def __init__(self, parent, message):
        super().__init__(parent)

        self.setWindowTitle("Error")

        QBtn = (
            QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    
    def __init__(self, shared_config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn_manager = DBConnectionManager()
        self._meta_data_reader = MetaDataReader(shared_config)
        self._query_service = QueryService(shared_config)
        self._current_fact_table = None
        self.setWindowTitle('Visualizator')
        self.resize(1400,700)

        # Graph
        self._canvas = MplCanvas(self, width=25, height=4, dpi=100)
        self._canvas.axes.yaxis.set_visible(False)
        self._canvas.axes.xaxis.set_visible(False)
        self._canvas.axes.set_xlabel('Date')
        self._build_ui()

        self._all_twin_axes = []
        for _ in range(10):
            new_twin_axis = self._canvas.axes.twinx()
            new_twin_axis.yaxis.set_visible(False)
            new_twin_axis.set_ylim(bottom=0, top=10)
            self._all_twin_axes.append(new_twin_axis)

        self._colors = [
            "royalblue",
            "tomato",
            "mediumseagreen",
            "gold",
            "mediumpurple",
            "deeppink",
            "darkturquoise",
            "coral",
            "slateblue",
            "limegreen"
        ]

    def show(self): 
        self._fact_selection.clear()
        try:
            self._fact_selection.addItems(self._meta_data_reader.get_fct_tables())
        except psycopg.OperationalError:
            dlg = CustomDialog(self, "Database connection failed.")
            dlg.exec()
            return
        self._clearLayout(self._sensor_layout)
        self._clearLayout(self._metric_layout)
        self._clear_axes()
        super().show()

    def closeEvent(self, event: QCloseEvent):
        if not self._conn_window.isVisible():
            self._conn_manager.close_connection_if_exists()
        event.accept()

    def set_conn_window(self, conn_window):
        self._conn_window = conn_window

    def _build_ui(self):

        # CREATING CONTAINERS
        main_container = QWidget()
        self.setCentralWidget(main_container)
        main_container_layout = QHBoxLayout()
        main_container.setLayout(main_container_layout)
        
        control_container = QWidget()
        control_container_layout = QVBoxLayout()
        control_container.setLayout(control_container_layout)
        main_container_layout.addWidget(control_container)

        graph_container = QWidget()
        graph_container.setMinimumWidth(400)
        graph_container_layout = QVBoxLayout()
        graph_container.setLayout(graph_container_layout)
        main_container_layout.addWidget(graph_container)

        # setting ratio between control part and graph part
        main_container_layout.addWidget(control_container, stretch=3)
        main_container_layout.addWidget(graph_container, stretch=8)
        
        # GRAPH PART
        graph_container_layout.addWidget(self._canvas)

        # CONTROL PART
        # set connection button
        connection_button = QPushButton('<< Set connection')
        connection_button.clicked.connect(self._on_set_clicked)
        control_container_layout.addWidget(connection_button)

        # groupbox
        fct_table_selection = QGroupBox("Fact table selection")
        fct_table_selection_layout = QVBoxLayout()
        fct_table_selection.setLayout(fct_table_selection_layout)
        control_container_layout.addWidget(fct_table_selection)

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
        control_container_layout.addWidget(configuration)
        configuration_layout = QGridLayout()
        configuration.setLayout(configuration_layout)

        # start_datetime date label
        start_label = QLabel('Start date')
        start_label.setAlignment(Qt.AlignLeft)
        configuration_layout.addWidget(start_label,8,0)

        # start_datetime date selection
        self._start_date = QDateEdit()
        self._start_date.setCalendarPopup(True)
        self._start_date.setDate(QDate(2015,7,4))
        configuration_layout.addWidget(self._start_date,10,0)

        # end_datetime date label
        end_label = QLabel('End date')
        end_label.setAlignment(Qt.AlignLeft)
        configuration_layout.addWidget(end_label,8,1)

        # end_datetime date selection
        self._end_date = QDateEdit()
        self._end_date.setCalendarPopup(True)
        self._end_date.setDate(QDate(2015,7,6))
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

        # clear 
        load_button = QPushButton('Clear')
        load_button.clicked.connect(self._clear_axes)
        configuration_layout.addWidget(load_button,30,1)

    def _on_show_clicked(self):
        if self._fact_selection.count() == 0:
            dlg = CustomDialog(self, "Fact table was not selected")
            dlg.exec()
            return
        self._current_fact_table = self._fact_selection.currentText()
        try:
            sensors = self._meta_data_reader.get_sensors(self._current_fact_table)
            metrics = self._meta_data_reader.get_metrics(self._current_fact_table)
        except psycopg.OperationalError:
            dlg = CustomDialog(self, "Database connection failed.")
            dlg.exec()
            return

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

    def _clear_axes(self):
        for axes in self._all_twin_axes:
            axes.yaxis.set_visible(False)
            axes.cla()
        # musel som tu pridat tento druhy cyklus na to, aby to spravne cistilo osi
        # mozno sa to da aj inak, ale neviem teraz na to prist
        for axes in self._all_twin_axes:
            axes.cla()
        for legend in self._canvas.figure.legends:
            legend.remove()
        self._canvas.figure.subplots_adjust(right=0.9, left=0.03)
        self._canvas.axes.xaxis.set_visible(False)
        self._canvas.draw()

    def _on_load_clicked(self):

        if self._current_fact_table == None:
            dlg = CustomDialog(self, "Please select a fact table first")
            dlg.exec()
            return

        start_date = self._start_date.date().toPython()
        end_date = self._end_date.date().toPython()

        start_datetime = datetime(start_date.year, start_date.month, start_date.day)
        end_datetime = datetime(end_date.year, end_date.month, end_date.day)

        if start_datetime > end_datetime:
            dlg = CustomDialog(self, "Start date must be before end date")
            dlg.exec()
            return

        chosen_sensors = []
        chosen_metrics = []

        for cb in self._sensor_checkboxes:
            if cb.isChecked():
                chosen_sensors.append(cb.text())
        
        for cb in self._metric_checkboxes:
            if cb.isChecked():
                chosen_metrics.append(cb.text())

        if len(chosen_metrics) > 10:
            dlg = CustomDialog(self, "Please select maximum 10 metrics")
            dlg.exec()
            return

        if len(chosen_sensors) == 0:
            dlg = CustomDialog(self, "Please select at least one sensor")
            dlg.exec()
            return
        
        if len(chosen_metrics) == 0:
            dlg = CustomDialog(self, "Please select at least one metric")
            dlg.exec()
            return

        # one metric, many sensors
        elif len(chosen_sensors) > 0 and len(chosen_metrics) == 1:

            try:
                metric_values_for_sensors = self._query_service.get_data_many_sensors_one_metric(self._current_fact_table, chosen_sensors, chosen_metrics[0], start_datetime, end_datetime)
            except psycopg.OperationalError:
                dlg = CustomDialog(self, "Database connection failed.")
                dlg.exec()
                return

            x = []
            current_datetime = start_datetime
            while current_datetime <= end_datetime + timedelta(days=1):
                x.append(current_datetime)
                current_datetime += timedelta(hours=1)

            indices = [0 for _ in range(len(chosen_sensors))]
            y = [[] for _ in range(len(chosen_sensors))]
            for date_time in x:
                for i in range(len(chosen_sensors)):
                    if indices[i] < len(metric_values_for_sensors[i]) and metric_values_for_sensors[i][indices[i]][0] == date_time:
                        y[i].append(metric_values_for_sensors[i][indices[i]][1])
                        indices[i] += 1
                    else:
                        y[i].append(np.nan)
                
            self._clear_axes()
            self._canvas.axes.xaxis.set_visible(True)

            y_len = len(y)

            self._all_twin_axes[0].set_ylabel(chosen_metrics[0], color="black")
            self._all_twin_axes[0].yaxis.set_label_position("right")
            
            for i in range(y_len):
                print(x)
                print()
                print(y)
                print("\n\n\n\n")
                self._all_twin_axes[0].plot(x, y[i], self._colors[i], label=chosen_sensors[i])

            # creating legend
            lines = []
            labels = []
            for i in range(y_len):
                new_lines, new_labels = self._all_twin_axes[i].get_legend_handles_labels()
                lines.extend(new_lines)
                labels.extend(new_labels)
            self._canvas.figure.legend(lines, labels, loc='upper center', ncol=4)

            self._all_twin_axes[0].tick_params('y', colors='black', labelsize=8)

            self._all_twin_axes[0].yaxis.set_visible(True)

            self._canvas.draw()
        
        # one sensor, many metrics
        elif len(chosen_sensors) == 1 and len(chosen_metrics) > 0:    

            try:
                timestamp_measurements = self._query_service.get_data_one_sensor_many_metrics(self._current_fact_table, chosen_sensors[0], chosen_metrics, start_datetime, end_datetime)
            except psycopg.OperationalError:
                dlg = CustomDialog(self, "Database connection failed.")
                dlg.exec()
                return

            # creating list for x axis
            # creating list for y axis
            i = 0
            x = []
            y_len = len(chosen_metrics)
            y = [[] for _ in range(y_len)]
            current_datetime = start_datetime
            while current_datetime < end_datetime + timedelta(days=1):
                
                x.append(current_datetime)

                if i < len(timestamp_measurements) and timestamp_measurements[i][0] == current_datetime:
                    for j in range(y_len):
                        y[j].append(timestamp_measurements[i][j+1])
                    i += 1
                else:
                    for j in range(y_len):
                        y[j].append(np.nan)
                current_datetime += timedelta(hours=1)

            self._clear_axes()
            self._canvas.axes.xaxis.set_visible(True)

            for i in range(y_len):

                self._all_twin_axes[i].plot(x, y[i], self._colors[i], label=chosen_metrics[i])
                self._all_twin_axes[i].spines['right'].set_position(('outward', i*45))
                self._all_twin_axes[i].set_ylabel(chosen_metrics[i], color=self._colors[i], fontsize=8)
                self._all_twin_axes[i].yaxis.set_label_position("right")
                self._all_twin_axes[i].tick_params('y', colors=self._colors[i], labelsize=8)
                self._all_twin_axes[i].yaxis.set_visible(True)

            self._canvas.figure.subplots_adjust(right=0.9 - (y_len - 1) * 0.06, left=0.03)

            self._canvas.draw()

        else:
            dlg = CustomDialog(self, "Select one sensor with multiple metrics, or one metric with multiple sensors")
            dlg.exec()
            return
    

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