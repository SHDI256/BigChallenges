from generatory import calc_high_relu, calc_high_low, calc_low_relu
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QRadioButton, QLineEdit, QSpinBox, QFileDialog, QErrorMessage
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from generator_pictures import generator
import cv2
from image.image_processing import numpy_to_bytes
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QTimer, QThreadPool, QRunnable
from PyQt5.QtGui import QImage, QPixmap
from generator_pictures import generator

from client_api import Registration
from nn_scripts.main import mod_frame

from vars import HOST, PORT2


transfer = Registration(HOST, PORT2)
# data_transfer_


class ThreadP(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # global times
        for photo in generator():
            h, w, ch = photo.shape
            self.photo = photo
            photo = mod_frame(photo)
            bytesPerLine = ch * w
            convertToQtFormat = QImage(photo.data, w, h, bytesPerLine, QImage.Format_RGB888)
            # p = convertToQtFormat.scaled(int(640 // 2.2), int(360 // 2.2), Qt.KeepAspectRatio)
            self.changePixmap.emit(convertToQtFormat)


class PhotoWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setFixedSize(1280, 720)

        self.label = QLabel(self)
        self.label.resize(1280, 720)
        self.label.move(0, 0)

        self.th = ThreadP(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        button = QPushButton('Take', self)
        button.setGeometry(1230, 670, 50, 50)
        button.setStyleSheet('background-color: #396eeb; border-radius: 10px;')
        button.clicked.connect(self.take)

    def take(self):
        mainWin.file = self.th.photo
        mainWin.file_changed = True
        self.destroy()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.sex = True

        self.setMinimumSize(QSize(300, 380))
        self.setFixedSize(300, 380)
        self.setWindowTitle("Registration")
        self.formula = 0
        bias = -80

        self.setStyleSheet('background-color: #1d203f')
        background = QLabel('', self)
        background.setGeometry(30, 10, 240, 360)
        background.setStyleSheet('background-color: #2d325c; border-radius: 10;')

        pybutton = QPushButton('Take a photo', self)
        pybutton.clicked.connect(self.take_a_photo)
        pybutton.resize(200, 50)
        pybutton.move(50, 330 + bias)
        pybutton.setStyleSheet('background-color: #396eeb; border-radius: 10px;')

        pybutton = QPushButton('Register', self)
        pybutton.clicked.connect(self.signup)
        pybutton.resize(200, 50)
        pybutton.move(50, 330 + 60 + bias)
        pybutton.setStyleSheet('background-color: #396eeb; border-radius: 10px;')

        radiobutton = QRadioButton("Male", self)
        radiobutton.setChecked(True)
        radiobutton.toggled.connect(self.male)
        radiobutton.setGeometry(50, 250 + bias, 200, 30)
        radiobutton.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        radiobutton = QRadioButton("Female", self)
        radiobutton.toggled.connect(self.female)
        radiobutton.setGeometry(50, 280 + bias, 200, 30)
        radiobutton.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        self.name = QLineEdit(self)
        self.name.setPlaceholderText('Name')
        self.name.setGeometry(50, 100 + bias, 200, 30)
        self.name.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        self.surname = QLineEdit(self)
        self.surname.setPlaceholderText('Surname')
        self.surname.setGeometry(50, 130 + bias, 200, 30)
        self.surname.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        age_label = QLabel('Age:', self)
        age_label.setGeometry(50, 160 + bias, 200, 30)
        age_label.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        self.age = QSpinBox(self)
        self.age.setGeometry(50, 190 + bias, 200, 30)
        self.age.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        sex_label = QLabel('Sex:', self)
        sex_label.setGeometry(50, 220 + bias, 200, 30)
        sex_label.setStyleSheet('color: white; padding-left: 3px; background-color: #2d325c;')

        self.file = None
        self.file_changed = False
        self.window = PhotoWindow()
        self.err = QErrorMessage()

    def male(self):
        self.sex = True

    def female(self):
        self.sex = False

    def take_a_photo(self):
        # for i in generator():
        #     self.file = i
        #     break
        # cv2.imshow('You are', cv2.cvtColor(self.file, cv2.COLOR_BGR2RGB))
        # print(self.file.shape)
        self.window.show()
        # self.signup()

    def signup(self):
        if self.file_changed:
            name = self.name.text()
            surname = self.surname.text()
            age = self.age.value()
            file = self.file
            transfer.open()
            transfer.data_transfer_full_name([name, surname])
            transfer.data_transfer_age(age)
            transfer.data_transfer_sex(bool(self.sex))
            transfer.data_transfer_photo(numpy_to_bytes(file))
            transfer.close()
            self.name.setText('')
            self.surname.setText('')
            self.age.setValue(0)
            self.file = None
            self.file_changed = False
        else:
            self.err.showMessage('Take a photo')


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        mainWin = MainWindow()
        mainWin.show()
        app.exec()
    except Exception as e:
        print(e)
