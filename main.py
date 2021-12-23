# Initial window made following https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QFormLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)


        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Button connected to plot method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # text boxes to enter function, min x, and max x

        self.functionLineEdit = QLineEdit(self)
        self.minXLineEdit = QLineEdit(self)
        self.maxXLineEdit = QLineEdit(self)

        # set the layout
        generalLayout = QVBoxLayout()
        formLayout = QFormLayout()
        generalLayout.addWidget(self.toolbar)
        generalLayout.addWidget(self.canvas)
        generalLayout.addLayout(formLayout)
        formLayout.addWidget(self.button)
        formLayout.addRow("Function to Plot", self.functionLineEdit)
        formLayout.addRow("Maximum value of x", self.minXLineEdit)
        formLayout.addRow("Minimum value of x", self.maxXLineEdit)
        self.setLayout(generalLayout)

    def plot(self):
        data = [i**2 for i in range(100)]

        self.figure.clear()

        # Create an axis
        ax = self.figure.add_subplot(111)

        # plot the data
        ax.plot(data)

        # Refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Styles
    app.setStyleSheet("""
        QLabel, QLineEdit {
            font-size: 10pt;
        }
    """)

    main = Window()
    main.show()

    sys.exit(app.exec_())