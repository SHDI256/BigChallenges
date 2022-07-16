import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QListView, QPushButton, QLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QTimer, QThreadPool, QRunnable
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtGui
from generatory import generator, tgenerator, generator2
import numpy as np
from datetime import datetime
from vars import HOST, PORT1
from client_api import Transfer


times = []
accept = None


class ThreadP(QThread):
    changePixmap = pyqtSignal(QImage)
    changeList = pyqtSignal(list)

    def run(self):
        global times
        for vector, photo in generator2():

            times.append(datetime.now())
            try:
                times = list(filter(lambda x: abs(x.timestamp() - datetime.now().timestamp()) < 60, times))
                print(f'{(len(times) / abs(times[0].timestamp() - times[-1].timestamp())):.2f}')
            except Exception as e:
                print(e)

            h, w, ch = photo.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(photo.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            self.changeList.emit(vector)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'AntiScam'
        self.initUI()
        self.update()


    def accept(self):
        transfer = Transfer(HOST, PORT1)
        transfer.open()
        transfer.data_transfer_verdict(True)
        transfer.close()

    def reject(self):
        transfer = Transfer(HOST, PORT1)
        transfer.open()
        transfer.data_transfer_verdict(False)
        transfer.close()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(list)
    def setParamters(self, spisok):
        accept_style = 'background-color: #396eeb; color: white; padding-left: 3px;'
        reject_style = 'background-color: #e86099; color: white; padding-left: 3px;'
        info_style = 'color: white; padding-left: 3px; background-color: #2d325c;'
        predict_accept_style = 'color: white; padding-left: 3px; background-color: #2d325c; border-radius: 10px;'
        predict_reject_style12 = 'color: white; padding-left: 3px; background-color: #e86099; border-radius: 10px;'
        predict_reject_style23 = 'color: white; padding-left: 3px; background-color: #b83069; border-radius: 10px;'
        predict_reject_style34 = 'color: white; padding-left: 3px; background-color: #980039; border-radius: 10px;'
        alarm = 40
        predict_alarm = 20
        predict_alarm2 = 50
        predict_alarm3 = 75
        predict_alarm4 = 100
        par1, par2, par3, par4, par5, par6, par7, par8, par9, par10, par11, interest = spisok
        predict = sum(map(abs, interest[:])) / len(interest[:])
        # self.parmameter1.setText(par1)
        self.parmameter1.setText('Имя: Миша')
        self.parmameter1.setStyleSheet(info_style + ' border-top-left-radius: 10px; border-top-right-radius: 10px;')
        # self.parmameter2.setText(par2)
        self.parmameter2.setText('Возраст: 16 лет')
        self.parmameter2.setStyleSheet(info_style)
        # self.parmameter3.setText(par3)
        self.parmameter3.setText('Пол: Мужской')
        self.parmameter3.setStyleSheet(info_style + ' border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;')
        self.parmameter4.setText(par4)
        if abs(interest[0]) <= alarm:
            self.parmameter4.setStyleSheet(accept_style + ' border-top-left-radius: 10px; border-top-right-radius: 10px;')
        else:
            self.parmameter4.setStyleSheet(reject_style + ' border-top-left-radius: 10px; border-top-right-radius: 10px;')
        self.parmameter5.setText(par5)
        if abs(interest[1]) <= alarm:
            self.parmameter5.setStyleSheet(accept_style)
        else:
            self.parmameter5.setStyleSheet(reject_style)
        self.parmameter6.setText(par6)
        if abs(interest[2]) <= alarm:
            self.parmameter6.setStyleSheet(accept_style)
        else:
            self.parmameter6.setStyleSheet(reject_style)
        self.parmameter7.setText(par7)
        if abs(interest[3]) <= alarm:
            self.parmameter7.setStyleSheet(accept_style)
        else:
            self.parmameter7.setStyleSheet(reject_style)
        self.parmameter8.setText(par8)
        if abs(interest[4]) <= alarm:
            self.parmameter8.setStyleSheet(accept_style)
        else:
            self.parmameter8.setStyleSheet(reject_style)
        self.parmameter9.setText(par9)
        if abs(interest[5]) <= alarm:
            self.parmameter9.setStyleSheet(accept_style)
        else:
            self.parmameter9.setStyleSheet(reject_style)
        self.parmameter10.setText(par10)
        if abs(interest[6]) <= alarm:
            self.parmameter10.setStyleSheet(accept_style)
        else:
            self.parmameter10.setStyleSheet(reject_style)
        self.parmameter11.setText(par11)
        if abs(interest[7]) <= alarm:
            self.parmameter11.setStyleSheet(accept_style + ' border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;')
        else:
            self.parmameter11.setStyleSheet(reject_style + ' border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;')
        if predict <= predict_alarm:
            self.predict.setText(f'Predict: {predict:.2f}% - Спокойный')
            self.predict.setStyleSheet(predict_accept_style)
        elif predict <= predict_alarm2:
            self.predict.setText(f'Predict: {predict:.2f}% - В стрессе')
            self.predict.setStyleSheet(predict_reject_style12)
        elif predict <= predict_alarm3:
            self.predict.setText(f'Predict: {predict:.2f}% - В сильном стрессе')
            self.predict.setStyleSheet(predict_reject_style23)
        elif predict <= predict_alarm4:
            self.predict.setText(f'Predict: {predict:.2f}% - Особо опасен')
            self.predict.setStyleSheet(predict_reject_style34)

    def initUI(self):
        self.setStyleSheet('background-color: #1d203f')
        self.setWindowTitle(self.title)
        # create a label
        self.label = QLabel(self)
        self.label.resize(640, 360)
        self.setFixedSize(1100, 450)
        # self.parmameters_layout = QLayout(self)

        self.accept_button = QPushButton(self)
        self.accept_button.setText('Accept')
        self.accept_button.setStyleSheet('background-color: #396eeb; border-bottom-left-radius: 10px; border-top-left-radius: 10px;')
        self.reject_button = QPushButton(self)
        self.reject_button.setText('Reject')
        self.reject_button.setStyleSheet('background-color: #e86099; border-bottom-right-radius: 10px; border-top-right-radius: 10px;')
        self.accept_button.setGeometry(0, 380, 320, 70)
        self.reject_button.setGeometry(320, 380, 320, 70)
        self.accept_button.clicked.connect(self.accept)
        self.reject_button.clicked.connect(self.reject)

        self.predict = QLabel(self)
        self.predict.setText('Predict: ')
        self.predict.setGeometry(660, 380, 440, 70)
        self.parmameter1 = QLabel(self)
        self.parmameter2 = QLabel(self)
        self.parmameter3 = QLabel(self)
        self.parmameter4 = QLabel(self)
        self.parmameter5 = QLabel(self)
        self.parmameter6 = QLabel(self)
        self.parmameter7 = QLabel(self)
        self.parmameter8 = QLabel(self)
        self.parmameter9 = QLabel(self)
        self.parmameter10 = QLabel(self)
        self.parmameter11 = QLabel(self)
        self.parmameter1.setText('Parameter1: ')
        self.parmameter2.setText('Parameter2: ')
        self.parmameter3.setText('Parameter3: ')
        self.parmameter4.setText('Parameter4: ')
        self.parmameter5.setText('Parameter5: ')
        self.parmameter6.setText('Parameter6: ')
        self.parmameter7.setText('Parameter7: ')
        self.parmameter8.setText('Parameter8: ')
        self.parmameter9.setText('Parameter9: ')
        self.parmameter10.setText('Parameter10: ')
        self.parmameter11.setText('Parameter11: ')

        self.parmameter1.setGeometry(660, 10, 440, 30)
        self.parmameter2.setGeometry(660, 40, 440, 30)
        self.parmameter3.setGeometry(660, 70, 440, 30)
        self.parmameter4.setGeometry(660, 120, 440, 30)
        self.parmameter5.setGeometry(660, 150, 440, 30)
        self.parmameter6.setGeometry(660, 180, 440, 30)
        self.parmameter7.setGeometry(660, 210, 440, 30)
        self.parmameter8.setGeometry(660, 240, 440, 30)
        self.parmameter9.setGeometry(660, 270, 440, 30)
        self.parmameter10.setGeometry(660, 300, 440, 30)
        self.parmameter11.setGeometry(660, 330, 440, 30)

        # self.parmameters_layout.addWidget(self.parmameter1)
        # self.parmameters_layout.addWidget(self.parmameter2)
        # self.parmameters_layout.addWidget(self.parmameter3)
        # self.parmameters_layout.addWidget(self.parmameter4)
        # self.parmameters_layout.addWidget(self.parmameter5)
        # self.parmameters_layout.addWidget(self.parmameter6)
        # self.parmameters_layout.addWidget(self.parmameter7)
        # self.parmameters_layout.addWidget(self.parmameter8)
        # self.parmameters_layout.addWidget(self.parmameter9)
        # self.parmameters_layout.addWidget(self.parmameter10)
        # self.parmameters_layout.addWidget(self.parmameter11)
        #
        # self.parmameters_layout.set

        th = ThreadP(self)
        th.changePixmap.connect(self.setImage)
        th.changeList.connect(self.setParamters)
        th.start()
        self.show()

        app.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
