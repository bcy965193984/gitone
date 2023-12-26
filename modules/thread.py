from signal import *
from PyQt5.QtCore import QThread
from robot import *
class threadrobot(QThread):
    getph=Getphoto_signal()
    def run(self):
        ws_address = "ws://192.168.18.180:8000/subscribe"
        client = MyWebSocket(ws_address,getph)
        client.connect_to_websocket(ws_address)