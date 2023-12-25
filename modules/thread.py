from threading import *
from PyQt5.QtCore import QThread
from robot import *
class threadrobot(QThread):
    def run(self):
        ws_address = "ws://192.168.18.180:8000/subscribe"
        client = MyWebSocket(ws_address)
        client.connect_to_websocket(ws_address)