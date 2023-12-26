from PyQt5.QtCore import pyqtSignal,QObject

class Getphoto_signal(QObject):
    getphoto_signal=pyqtSignal()
# 发射信号
#   getph=Getphoto_signal()
#   getph.getphoto_signal.emit()