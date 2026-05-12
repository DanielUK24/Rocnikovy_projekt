import os

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QScrollArea, QCheckBox, QGridLayout, QPushButton, QComboBox
from PySide6.QtCore import Qt, QDate

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    
    def __init__(self, set_connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Visualizator')
        self._set_connection = set_connection

        self._build_ui()

    def _build_ui(self):

        control_graph_container = QWidget()
        self.setCentralWidget(control_graph_container)
        container_layout = QHBoxLayout()
        control_graph_container.setLayout(container_layout)

        control_panel = QWidget()
        container_layout.addWidget(control_panel)

        control_layout = QGridLayout()
        control_panel.setLayout(control_layout)

        # set connection button
        connection_button = QPushButton('<< Set connection')
        connection_button.clicked.connect(self._on_set_clicked)
        control_layout.addWidget(connection_button)

        # fact table selection label
        fact_label = QLabel('Select fact table')
        fact_label.setAlignment(Qt.AlignLeft)
        control_layout.addWidget(fact_label,2,0)

        # fact table selection
        fact_selection = QComboBox()
        fact_selection.addItems(['fct_weather', 'fct_water'])
        control_layout.addWidget(fact_selection,5,0)

        # show button
        show_button = QPushButton('Show')
        #show_button.clicked.connect()
        control_layout.addWidget(show_button,6,0)

        # start date label
        start_label = QLabel('Start date')
        start_label.setAlignment(Qt.AlignLeft)
        control_layout.addWidget(start_label,8,0)

        # start date selection
        self._start_date = QDateEdit()
        self._start_date.setCalendarPopup(True)
        self._start_date.setDate(QDate(2014,6,1))
        control_layout.addWidget(self._start_date,10,0)

        # end date label
        end_label = QLabel('End date')
        end_label.setAlignment(Qt.AlignLeft)
        control_layout.addWidget(end_label,8,1)

        # end date selection
        self._end_date = QDateEdit()
        self._end_date.setCalendarPopup(True)
        self._end_date.setDate(QDate(2014,6,10))
        control_layout.addWidget(self._end_date,10,1)

        # sensor and metric selection label
        sensor_metric_label = QLabel("Select")
        sensor_metric_label.setAlignment(Qt.AlignLeft)
        sensor_metric_label.setToolTip('''
            Choose items so that one list has exactly one selection 
            while the other has one or more selections.
            You may choose which list has the single selection.
        ''')
        control_layout.addWidget(sensor_metric_label,15,0)

        # sensor selection
        sensor_scroll = QScrollArea()
        sensor_scroll.setWidgetResizable(True)

        sensor_container = QWidget()
        sensor_layout = QVBoxLayout(sensor_container)
        
        # toto sa bude vytvarat v osobitnej funkcii po stlaceni show
        k = """
        for i in range(100):
            cb = QCheckBox(f"Option {i}")
            sensor_layout.addWidget(cb)"""

        sensor_layout.addStretch()
        
        sensor_scroll.setWidget(sensor_container)
        
        control_layout.addWidget(sensor_scroll,20,0)

        # metric selection
        metric_scroll = QScrollArea()
        metric_scroll.setWidgetResizable(True)

        metric_container = QWidget()
        metric_layout = QVBoxLayout(metric_container)
        
        # toto sa bude vytvarat v osobitnej funkcii po stlaceni show
        k = """
        for i in range(100):
            cb = QCheckBox(f"Option {i}")
            metric_layout.addWidget(cb)"""

        metric_layout.addStretch()
        
        metric_scroll.setWidget(metric_container)
        
        control_layout.addWidget(metric_scroll,20,1)

        # load button
        load_button = QPushButton('Load')
        load_button.clicked.connect(self._on_load_clicked)
        control_layout.addWidget(load_button,30,0)

        # graph part
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        container_layout.addWidget(sc)

    def _read_filter():
        pass

    def _on_load_clicked(self):

        filter = self._read_filter()

        x, y = self.data_service.get_chart_data(filter)

        self.chart_service.plot(self.canvas, x, y)

    def _on_set_clicked(self):
        self._set_connection()