import os
import sys
import numpy as np

os.environ["QT_API"] = "PySide6"

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(1000, 600)

        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.exp(-x)
        y3 = 100 * np.cos(x)
        y4 = x**2
        y5 = np.log(x + 1)
        y6 = np.sqrt(x)
        y7 = 10 * np.tan(x / 5)

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        ax1 = sc.axes

        ax1.plot(x, y1, 'b', label='y1 (sin(x)')
        ax1.set_xlabel('X-axis')
        ax1.set_ylabel('y1', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()

        ax2.plot(x, y2, 'g', label='y2 (exp(-x))')
        ax2.set_ylabel('y2', color='g')
        ax2.tick_params('y', colors='g')

        ax3 = ax1.twinx()

        ax3.plot(x, y3, 'r', label='y3 (100*cos(x))')
        ax3.spines['right'].set_position(('outward', 60))
        ax3.set_ylabel('y3', color='r')
        ax3.tick_params('y', colors='r')

        ax4 = ax1.twinx()

        ax4.plot(x, y4, 'r', label='y4')
        ax4.spines['right'].set_position(('outward', 120))
        ax4.set_ylabel('y4')
        ax4.tick_params('y')

        ax5 = ax1.twinx()

        ax5.plot(x, y5, 'r', label='y5')
        ax5.spines['right'].set_position(('outward', 180))
        ax5.set_ylabel('y5')
        ax5.tick_params('y')

        ax6 = ax1.twinx()

        ax6.plot(x, y6, 'r', label='y6')
        ax6.spines['right'].set_position(('outward', 240))
        ax6.set_ylabel('y6')
        ax6.tick_params('y')

        ax7 = ax1.twinx()

        ax7.plot(x, y7, 'r', label='y7')
        ax7.spines['right'].set_position(('outward', 300))
        ax7.set_ylabel('y7')
        ax7.tick_params('y')

        sc.figure.subplots_adjust(right=0.4)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()