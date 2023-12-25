from modules import *
import sys
user_now=''
vip_account='724'
vip_password='724'
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=mainwindow(vip_account)
    sys.exit(app.exec())
