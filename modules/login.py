from mainwindow import *


#***************
#   登录界面
#***************
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_login()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow=QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0,0)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(Qt.black)
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.ui.pushButton_login.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_L_sure.clicked.connect(self.Login_in)
        self.ui.pushButton_R_register.clicked.connect((self.register))
        self.show()
    # ***************
    #      注册
    # ***************
    def register(self):
        account=self.ui.lineEdit_R_account.text()
        password_1=self.ui.lineEdit_R_password1.text()
        password_2=self.ui.lineEdit_R_password2.text()
        if len(account)==0 or len(password_1)==0 or len(password_2)==0:
            self.ui.stackedWidget.setCurrentIndex(1)
        elif password_2!=password_1:
            self.ui.stackedWidget.setCurrentIndex(3)
        else:
            self.ui.stackedWidget.setCurrentIndex(5)
            conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
            cur = conn.cursor()
            cur.execute("select * from users")
            rows = cur.fetchall()
            wrong=0
            for row in rows:
                if account==row[0]:
                    self.ui.stackedWidget.setCurrentIndex(4)
                    wrong=1
            if wrong==0:
                cur.execute(f"insert into users values('{account}','{password_1}')")
            conn.commit()
            conn.close()
    # ***************
    #      登录
    # ***************
    def Login_in(self):
        global user_now
        account=self.ui.lineEdit_L_account.text()
        password=self.ui.lineEdit_L_password.text()
        conn=psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur=conn.cursor()
        cur.execute("select * from users")
        rows=cur.fetchall()
        wrong=1
        if account==vip_account and password==vip_password:
            user_now = account
            self.close()
            self.win = mainwindow.mainwindow()

            wrong = 0
        self.ui.stackedWidget.setCurrentIndex(0)
        if len(account)==0 or len(password)==0:
            self.ui.stackedWidget.setCurrentIndex(1)
            wrong=0
        for row in rows:
            if account == row[0] and password == row[1]:
                user_now=account
                self.close()
                self.win = mainwindow.mainwindow()

                wrong=0
        if wrong==1:
            self.ui.stackedWidget.setCurrentIndex(2)
        print(rows)
        conn.commit()
        conn.close()