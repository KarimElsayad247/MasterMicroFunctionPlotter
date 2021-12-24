# Initial window made following https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies

import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QFormLayout, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import sympy as sym
from sympy.parsing.sympy_parser import standard_transformations
from sympy.parsing.sympy_parser import implicit_multiplication_application
from sympy.parsing.sympy_parser import convert_xor

import numpy as np

def parse_function(text):
    """parses incoming text and returns a sympy expression"""
    transformations = (standard_transformations + (convert_xor, implicit_multiplication_application))
    expression = sym.parse_expr(text, transformations=transformations, evaluate=False)
    return expression


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
        self.functionLineEdit.setValidator(QRegExpValidator(QRegExp("[ ()Eex+*-^\d]*")))

        self.minXLineEdit = QLineEdit(self)
        self.minXLineEdit.setValidator(QIntValidator())

        self.maxXLineEdit = QLineEdit(self)
        self.maxXLineEdit.setValidator(QIntValidator())

        # Label to display messages and errors
        self.errorsLabel = QLabel(self)
        self.errorsLabel.setText("Messages and errors go here")

        # set the layout
        generalLayout = QVBoxLayout()
        formLayout = QFormLayout()
        generalLayout.addWidget(self.toolbar)
        generalLayout.addWidget(self.canvas)
        generalLayout.addLayout(formLayout)
        formLayout.addWidget(self.button)
        formLayout.addRow("Function to Plot", self.functionLineEdit)
        formLayout.addRow("Minimum value of x", self.minXLineEdit)
        formLayout.addRow("Maximum value of x", self.maxXLineEdit)
        generalLayout.addWidget(self.errorsLabel)
        self.setLayout(generalLayout)

    def showError(self, errorText):
        self.errorsLabel.setStyleSheet("color: red")
        self.errorsLabel.setText(errorText)

    def showSuccess(self, sucessText):
        self.errorsLabel.setStyleSheet("color: green")
        self.errorsLabel.setText(sucessText)

    def plot(self):

        functionTextContent = self.functionLineEdit.text().replace('e', 'E')
        minX = self.minXLineEdit.text()
        maxX = self.maxXLineEdit.text()

        # Make sure user provides function, min x, and max x
        if not functionTextContent:
            self.showError("Function textbox can't be empty!")
            return False

        if not minX:
            self.showError("Must provide minimum value for x")
            return False

        if not maxX:
            self.showError("Must provide maximum value of x")
            return False

        try:
            expression = parse_function(functionTextContent)
        except ValueError:
            self.showError("Invalid expression for function!")
            return False

        x = sym.Symbol('x')
        if (len(expression.free_symbols) != 1) or (x not in expression.free_symbols):
            self.showError("Expression must contain only one variable and it must be x")
            return False

        minX = int(minX)
        maxX = int(maxX)

        print(expression, minX, maxX)

        resolution = 100
        xVals = np.linspace(minX, maxX, resolution)
        data = [expression.evalf(subs={x: i}) for i in xVals]

        self.figure.clear()

        # Create an axis
        ax = self.figure.add_subplot(111)

        # plot the data
        ax.plot(xVals, data)

        # Refresh canvas
        self.canvas.draw()

        self.showSuccess("Showing plot!")


    def fillWithTestData(self):
        self.functionLineEdit.setText("x + 1")
        self.minXLineEdit.setText("1")
        self.maxXLineEdit.setText("4")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Styles
    app.setStyleSheet("""
        QLabel, QLineEdit {
            font-size: 10pt;
        }
    """)

    main = Window()
    # main.fillWithTestData()
    main.show()

    sys.exit(app.exec_())
