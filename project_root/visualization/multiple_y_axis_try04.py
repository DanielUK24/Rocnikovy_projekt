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
        self.resize(960, 600)

        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.exp(-x)
        y3 = 100 * np.cos(x)
        y4 = x**2
        y5 = np.log(x + 1)
        y6 = np.sqrt(x)
        y7 = 10 * np.tan(x / 5)
        y8 = 10 * np.tan(x / 4)
        y9 = 10 * np.tan(x / 14)
        y10 = 10 * np.tan(x / 8)

        y_axes = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10]
        y_axes = y_axes[:6]

        sc = MplCanvas(self, width=5, height=4, dpi=100)

        ax0 = sc.axes
        ax0.yaxis.set_visible(False)

        colors = [
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

        y_axes_len = len(y_axes)

        for i in range(y_axes_len):

            ax = ax0.twinx()

            ax.plot(x, y_axes[i], colors[i], label='label1')
            ax.spines['right'].set_position(('outward', i*45))
            #ax.set_ylabel('label2', color=colors[i])
            ax.tick_params('y', colors=colors[i])

        sc.figure.subplots_adjust(right=0.9-(y_axes_len-1)*0.06)
        sc.figure.subplots_adjust(left=0.03)

        layout = QVBoxLayout()
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()