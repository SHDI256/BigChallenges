from generatory import calc_high_relu, calc_high_low, calc_low_relu
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 500))
        self.setWindowTitle("Tester")
        self.formula = 0

        pybutton = QPushButton('Calculate', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200, 50)
        pybutton.move(50, 400)

        radiobutton = QRadioButton("FUll formula", self)
        radiobutton.setChecked(True)
        radiobutton.toggled.connect(self.full)
        radiobutton.setGeometry(50, 300, 300, 30)

        radiobutton = QRadioButton("Low ReLU formula", self)
        radiobutton.toggled.connect(self.low_relu)
        radiobutton.setGeometry(50, 330, 300, 30)

        radiobutton = QRadioButton("High ReLU formula", self)
        radiobutton.toggled.connect(self.high_relu)
        radiobutton.setGeometry(50, 360, 300, 30)

        self.now = QLineEdit(self)
        self.now.setPlaceholderText('Now value: <float>')
        self.now.setGeometry(50, 100, 200, 30)

        self.before = QLineEdit(self)
        self.before.setPlaceholderText('Before values: <float>, <float>, ...')
        self.before.setGeometry(50, 140, 200, 30)

        self.mean = QLineEdit(self)
        self.mean.setPlaceholderText('Mean value: <float>')
        self.mean.setGeometry(50, 180, 200, 30)

        self.result = QLabel(self)
        self.result.setText(f'Δ')
        self.result.setGeometry(50, 250, 200, 30)

    def clickMethod(self):
        x = float(self.now.text())
        before = None
        if self.before.text().strip() != '':
            before = list(map(float, self.before.text().split(',')))
        mean = float(self.mean.text())
        if self.formula == 0:
            self.result.setText(f'Δ{calc_high_low(x, mean, before)}')
        elif self.formula == -1:
            self.result.setText(f'Δ{calc_low_relu(x, mean, before)}')
        elif self.formula == 1:
            self.result.setText(f'Δ{calc_high_relu(x, mean, before)}')


    def full(self):
        self.formula = 0

    def low_relu(self):
        self.formula = -1

    def high_relu(self):
        self.formula = 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
