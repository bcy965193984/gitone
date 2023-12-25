from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from thread import *
from ui import *
import time
import os
from chart import *
import cv2
import matplotlib.pyplot as plt
import sys
from login import *
signal_table=False
cwd=sys.argv[0]
n=0
exit=False
frame=None
from openpyxl import Workbook
user_now=''
vip_account='724'


#***************
#   主界面
#***************
class mainwindow(QMainWindow):
    refresh_single=pyqtSignal()
    def __init__(self,user):
        self.user_now=user
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()
        self.ui.stackedWidget_2.setCurrentIndex(0)
        self.guideLine()
        self.ui.pushButton_15.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_logout.clicked.connect(self.log_out)
        self.ui.pushButton_M_sure.clicked.connect((self.changepassword))
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.tableWidget.setSortingEnabled(True)
        self.historyTableSetUp()#历史记录表设置
        self.warningTableSetUp()#报警记录表设置
        self.ui.pushButton_close.clicked.connect(self.Close)
        self.ui.pushButton_east.clicked.connect(lambda: self.areaChange(self.ui.pushButton_east,0))
        self.ui.pushButton_west.clicked.connect(lambda: self.areaChange(self.ui.pushButton_west,1))
        #Thread(target=self.camerashow).start()
        #实时监控变化事件
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.stackedWidget_3.setCurrentIndex(1)
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(1))
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(0))
        self.thread=threadrobot()
        self.thread.start()


        #table初始化
        self.tableLinkSql()
        #图表重命名
        self.ui.tableWidget.itemChanged.connect(lambda: self.changetable(self.ui.tableWidget))
        #主界面读取摄像头文件
        self.mainUiLinkCamera()
        #数据分析界面
        self.dataAnlysisSetup()

        self.chartWindow01 = chart_ui()
        self.chartWindow02 = chart_ui()
        self.chart=self.chartWindow01

        self.ui.pushButton_daochu.clicked.connect(lambda: self.makeExcel())
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    def makeExcel(self):
        if 1==self.ui.stackedWidget_4.currentIndex():
            table=self.ui.tableWidget_4
        else:
            table=self.ui.tableWidget_3
        wb=Workbook()
        ws=wb.active
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                # 将QTable中的数据写入Excel文件
                ws.cell(row=row + 1, column=col + 1, value=str(table.item(row, col).text()))
        wb.save("output.xlsx")
    def areaChange(self,area,index):
        self.ui.pushButton_west.setStyleSheet("")
        self.ui.pushButton_east.setStyleSheet("")
        area.setStyleSheet("background-color: rgb(158, 158, 158);")
        self.ui.stackedWidget_6.setCurrentIndex(index)
    def dataAnlysisSetup(self):
        self.ui.stackedWidget_5.setCurrentIndex(0)
        self.ui.pushButton_duanlu.clicked.connect(lambda :self.duanlu())
        self.ui.pushButton_duanlu_2.clicked.connect(lambda: self.duanlu_2())
        # 作图
        self.chart()
        #按钮
        self.ui.pushButton_35.clicked.connect(lambda :self.makeChartUi(self.ui.comboBox_3,'OpenCircle'))
        self.ui.pushButton_37.clicked.connect(lambda: self.makeChartUi(self.ui.comboBox_4,'shortCircle'))
    def makeChartUi(self,box,type):
        self.chart.setWindowTitle(box.currentText())
        self.chart.show()
        self.type=type
        if(self.chart==self.chartWindow01):
            self.chart=self.chartWindow02
        else:
            self.chart = self.chartWindow01


    def chart(self):
        self.makeChart(self.ui.horizontalLayout_92,0,0)
        self.makeChart(self.ui.horizontalLayout_91,0,1)
        self.makeChart(self.ui.horizontalLayout_111,0,2)
        self.makeChart(self.ui.horizontalLayout_44,1,0)
        self.makeChart(self.ui.horizontalLayout_46,1,1)
        self.makeChart(self.ui.horizontalLayout_90,1,2)
    def makeChart(self,layout,status01,status02):
        wrong="ShortCircle"
        if(status01==1):
            wrong ="OpenCircle"
        type="week"
        if(status02==1):
            type = "mouth"
        elif(status02==2):
            type = "year"
        sql=f'{type}{wrong}'
        # 添加示例数据到图表容器
        x = []
        y = []
        self.chartContainer = pg.PlotWidget()
        layout.addWidget(self.chartContainer)
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute(f"select * from {sql} order by id ASC")
        rows = cur.fetchall()
        for row in rows:
           x.append(row[0])
           y.append(row[1])
        conn.commit()
        conn.close()

        self.chartContainer.setBackground('w')
        self.chartContainer.plot(x, y, pen='k')
        self.chartContainer.setTitle(type)
    def duanlu(self):
        self.ui.stackedWidget_5.setCurrentIndex(0)
        self.ui.pushButton_duanlu.setStyleSheet("QPushButton{background-color: rgb(209, 209, 209);}\n"
                                                "QPushButton:hover{background-color: rgb(209, 209, 209);}")
        self.ui.pushButton_duanlu_2.setStyleSheet("QPushButton:hover{background-color: rgb(209, 209, 209);}")
    def duanlu_2(self):
        self.ui.stackedWidget_5.setCurrentIndex(1)
        self.ui.pushButton_duanlu_2.setStyleSheet("QPushButton{background-color: rgb(209, 209, 209);}\n"
                                                  "QPushButton:hover{background-color: rgb(209, 209, 209);}")
        self.ui.pushButton_duanlu.setStyleSheet("QPushButton:hover{background-color: rgb(209, 209, 209);}")
    def tableLinkSql(self):
        global signal_table
        signal_table=True
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("select * from cameras order by id ASC")
        rows = cur.fetchall()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setIconSize(QSize(840, 500));
        for row in rows:
            tableHidth = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(tableHidth)
            self.ui.tableWidget.setRowHeight(tableHidth, 500)
            item = QTableWidgetItem()
            image = QImage(rf'{cwd}\..\Image mosaicking\{row[1]}.png')
            new_size = image.scaled(840, 500)
            item.setIcon(QIcon(QPixmap.fromImage(new_size)))
            self.ui.tableWidget.setItem(int(row[0]) - 1, 0, item)

            item = QTableWidgetItem(row[1])
            self.ui.tableWidget.setItem(int(row[0]) - 1, 1, item)

            self.ui.tableWidget.setRowHeight(int(row[0])-1,500)
        conn.commit()
        conn.close()
        signal_table=False

    def mainUiLinkCamera(self):
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("select * from cameras order by id ASC")
        rows = cur.fetchall()
        self.lastLabel=self.ui.label_11
        for row in rows:

            #self.ui.row[2].setPixmap(rf'{cwd}\..\cameras\{row[1]}.png')
            label = getattr(self.ui, row[2])
            def Event(event, name, label):

                pixmap = QPixmap(f'{cwd}\..\Image mosaicking\{name}.png')
                self.ui.label_show.setPixmap(pixmap)
                label.setStyleSheet('''border:5px solid rgb(0, 255, 0);''')
                if self.lastLabel!=label:
                    self.lastLabel.setStyleSheet('''''')
                self.lastLabel = label
                print("Mouse pressed!")

            def mouseReleaseEvent(event):
                print("Mouse released!")

            #label.setStyleSheet('''border:5px solid  rgb(255, 170, 0);''')
            #label.setScaledContents(True)
            label.setPixmap(QtGui.QPixmap(rf"{cwd}/../Image mosaicking/{row[1]}.png"))

            label.mousePressEvent = lambda event, arg1=row[1], arg2=label: Event(event, arg1, arg2)
            label.mouseReleaseEvent = mouseReleaseEvent
        conn.commit()
        conn.close()




    def guideLine(self):
        self.ui.pushButton_setup.clicked.connect(lambda: self.changeMainWindow(self.ui.pushButton_setup,0))  # lambda: self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.pushButton_dataAnlysis.clicked.connect(lambda: self.changeMainWindow(self.ui.pushButton_dataAnlysis, 4))
        self.ui.pushButton_my.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_outcome.clicked.connect(lambda: self.changeMainWindow(self.ui.pushButton_outcome, 3))
    def historyTableSetUp(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(f'{cwd}\..\history')
        self.model.setReadOnly(False)
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setRootIndex(self.model.index(f'{cwd}/../history'))
        self.ui.treeView.header().setStretchLastSection(True)
        self.ui.treeView.setAnimated(True)
        self.ui.history_photo_label.setScaledContents(True)
        self.ui.treeView.doubleClicked.connect(lambda: self.history_photo_show())
    def warningTableSetUp(self):
        self.ui.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.stackedWidget_4.setCurrentIndex(0)
        self.ui.pushButton_BaoJingJiLu.setStyleSheet("border:1px solid black;\n"
                                                     "border-bottom: none;\n"
                                                     "font: 16pt \"华文细黑\";\n"
                                                     "background-color: rgb(197, 12, 15);\n"
                                                     "padding-bottom:4px")
        self.ui.pushButton_BaoJingJiLu.clicked.connect(lambda: self.ui.stackedWidget_4.setCurrentIndex(0))
        self.ui.pushButton_BaoJingJiLu.clicked.connect(
            lambda: self.ui.pushButton_BaoJingJiLu.setStyleSheet("border:1px solid black;\n"
                                                                 "border-bottom: none;\n"
                                                                 "font: 16pt \"华文细黑\";\n"
                                                                 "background-color: rgb(197, 12, 15);\n"
                                                                 "padding-bottom:4px"))
        self.ui.pushButton_BaoJingJiLu.clicked.connect(
            lambda: self.ui.pushButton_BenCiBaoJing.setStyleSheet("border:1px solid black;\n"
                                                                  "border-bottom: none;\n"
                                                                  "background-color: rgb(231, 231, 231);\n"
                                                                  "font: 16pt \"华文细黑\";"))
        self.ui.pushButton_BenCiBaoJing.clicked.connect(lambda: self.ui.stackedWidget_4.setCurrentIndex(1))
        self.ui.pushButton_BenCiBaoJing.clicked.connect(
            lambda: self.ui.pushButton_BenCiBaoJing.setStyleSheet("border:1px solid black;\n"
                                                                  "border-bottom: none;\n"
                                                                  "font: 16pt \"华文细黑\";\n"
                                                                  "background-color: rgb(197, 12, 15);\n"
                                                                  "padding-bottom:4px"))
        self.ui.pushButton_BenCiBaoJing.clicked.connect(
            lambda: self.ui.pushButton_BaoJingJiLu.setStyleSheet("border:1px solid black;\n"
                                                                 "border-bottom: none;\n"
                                                                 "background-color: rgb(231, 231, 231);\n"
                                                                 "font: 16pt \"华文细黑\";"))
        self.ui.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.no_change_table(self.ui.tableWidget_3)
        self.no_change_table(self.ui.tableWidget_4)

    def space(self):
        return
    # ***************
    #     保存图片
    # ***************
    def save(self):
        global frame
        if frame==None:
            return
        time.time()
        t = time.localtime()
        year = t.tm_year
        month=t.tm_mon
        day=t.tm_mday
        fileName=f"{year}.{month}.{day}"
        global cwd
        path = f"{cwd}\..\spots\{fileName}"
        if os.path.exists(path)==False:
            os.mkdir(path)
        hour=t.tm_hour
        min=t.tm_min
        sec = t.tm_sec
        frame.save(f'{path}\{hour}.{min}.{sec}.png')

        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("select * from spots order by id")
        count=0
        rows = cur.fetchall()
        for row in rows:
            count+=1
        cur.execute(f"INSERT INTO spots VALUES ({count+1},'{hour}.{min}.{sec}' , '{path}')")
        conn.commit()
        conn.close()
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("select * from spots order by id ")
        rows = cur.fetchall()
        global signal_table
        signal_table=True
        tableHidth = self.ui.tableWidget.rowCount()
        for i in range(tableHidth):
            self.ui.tableWidget.removeRow(0)
            self.ui.tableWidget_2.removeRow(0)
        self.spots_link(self.ui.tableWidget_2)
        self.spots_link(self.ui.tableWidget)
        # self.ui.tableWidget.insertRow(tableHidth)
        # self.ui.tableWidget_2.insertRow(tableHidth)
        # for row in rows:
        #     item = QTableWidgetItem()
        #     item.setIcon(QIcon(QPixmap(f'{row[2]}\\{row[1]}.png')))
        #     self.ui.tableWidget.setItem(int(row[0]) - 1, 0, item)
        #     self.ui.tableWidget_2.setItem(int(row[0]) - 1, 0, item)
        #     item = QTableWidgetItem(row[1])
        #     self.ui.tableWidget.setItem(int(row[0]) - 1, 1, item)
        #     self.ui.tableWidget_2.setItem(int(row[0]) - 1, 1, item)
        # self.ui.tableWidget.setIconSize(QSize(300, 200))
        signal_table=False
        conn.commit()
        conn.close()

    def Close(self):
        global exit
        exit=True
        self.close()
    # ***************
    #     重命名
    # ***************
    def changetable(self,table):
        global signal_table
        if signal_table==True:
            return
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("select * from cameras order by id")
        rows = cur.fetchall()
        #table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        num=0
        for row in rows:
            if row[1]!=table.item(num,1).text():
                os.chdir(rf'{cwd}\..\Image mosaicking')
                os.rename(rf'{row[1]}.png',rf'{table.item(num,1).text()}.png')
            cur.execute(f"update cameras set name='{table.item(num,1).text()}' where id={num+1};")
            num+=1

        conn.commit()
        conn.close()
        h=table.rowCount()
        for i in range(h+1):
            self.ui.tableWidget.removeRow(0)
        self.tableLinkSql()

    def no_change_table(self,table):
        rowCount = table.rowCount()
        columnCount = table.columnCount()
        for i in range(rowCount):  # 结果界面表不可更改
            for j in range(rowCount):
                item = table.item(i, j)
                if item != None:
                       item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    #***************
    #     连接表
    #***************
    def spots_link(self,table):
        table.setIconSize(QSize(300, 200));
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("select * from spots order by id  ")
        rows=cur.fetchall()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row in rows:
            tableHidth = table.rowCount()
            table.insertRow(tableHidth)
            table.setRowHeight(tableHidth, 200)
            item = QTableWidgetItem()
            item.setIcon(QIcon(QPixmap(f'{row[2]}\\{row[1]}.png')))
            table.setItem(int(row[0])-1, 0,item)

            item = QTableWidgetItem(row[1])
            table.setItem(int(row[0])-1,1,item)

        conn.commit()
        conn.close()

    # ***************
    #   显示摄像头
    # ***************
    def camerashow(self):

        camera = cv2.VideoCapture(0)  # 捕获摄像头
        if camera.isOpened():  # 检查是否打开
            open, frame = camera.read()
            img = frame.copy()
        else:
            open = False
        while open:
            ret, frame = camera.read()  # ret为一个bool类型，frame为当前帧图像
            frame = cv2.flip(frame, 1)
            if frame is None:
                break
            if ret == True:
                self.Opencv_to_QPixmap(pic_show_label=self.ui.camera, img=frame)
                global exit
                #print(exit)
                if exit:
                    break
        camera.release()
        cv2.destroyAllWindows()


    # ***************
    #   显示历史图片
    # ***************
    def history_photo_show(self):
        index=self.ui.treeView.currentIndex()
        path=self.model.filePath(index)
        self.ui.history_photo_label.setPixmap(QPixmap(path))
        print(f'{path}')

    def Opencv_to_QPixmap(self, pic_show_label, img):
        #print('-----cvread_labelshow-----')

        # 图片路径
        #img_path = path

        # 通过cv读取图片  BGR格式
        #img = cv2.imread(img_path)
        #print('cv2 : ', type(img))  # cv2 :  <class 'numpy.ndarray'>
        plt.subplot(121)
        plt.title('BGR-格式')
        plt.imshow(img)  # img本来是BGR格式，通过img[:,:,::-1]转为RGB格式

        # 通道转化  BGR->RGB
        RGBImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(122)
        plt.title('RGB-格式')
        plt.imshow(RGBImg)  # matplotlib只能显示RGB图像
        plt.show()

        # 将图片转化成Qt可读格式   QImage
        qimage = QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], QImage.Format_RGB888)
        #print('qimage type:', type(qimage))
        piximage = QPixmap(qimage)
        #print('piximage type:', type(piximage))

        # 显示图片
        pic_show_label.setPixmap(piximage)
        pic_show_label.setScaledContents(True)
        self.ui.label_13.setPixmap((piximage))
        self.ui.label_13.setScaledContents(True)
        global frame
        frame=piximage
        #print('pic_show_label mess:', pic_show_label.width(), pic_show_label.height())
        #print('piximage mess:', piximage.width(), piximage.height())

    def send(self):
        while True:
            time.sleep(0.001)
            self.refresh_single.emit()

    # ***************
    #     改界面
    # ***************
    def changeMainWindow(self,button,n):
        if  n!=0 or self.user_now==vip_account:
            self.change()
            button.setStyleSheet("background-color:  rgb(236, 239, 241);\n"
                             "color: rgb(0, 0,107);")
            self.ui.stackedWidget.setCurrentIndex(n)
        elif n==0 and self.user_now!=vip_account:
            QMessageBox.information(self, '错误', '非管理员账户！', QMessageBox.Ok)

    def change(self):
        self.ui.pushButton_dataAnlysis.setStyleSheet("color: rgb(236, 239, 241);")
        self.ui.pushButton_my.setStyleSheet("color: rgb(236, 239, 241);")
        self.ui.pushButton_setup.setStyleSheet("color: rgb(236, 239, 241);")
        self.ui.pushButton_outcome.setStyleSheet("color: rgb(236, 239, 241);")

    # ***************
    #     改密码
    # ***************
    def changepassword(self):
        global user_now
        self.ui.stackedWidget_2.setCurrentIndex(0)
        if len(self.ui.lineEdit_M_pass_1.text()) == 0 or len(self.ui.lineEdit_M_pass_2.text())==0:
            self.ui.stackedWidget_2.setCurrentIndex(1)
        elif self.ui.lineEdit_M_pass_1.text()==self.ui.lineEdit_M_pass_2.text():
            self.ui.stackedWidget_2.setCurrentIndex(3)
            password=self.ui.lineEdit_M_pass_1.text()
            conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
            cur = conn.cursor()
            cur.execute(f"update users set passwords='{password}' where accounts='{user_now}'")
            conn.commit()
            conn.close()
        else:
            self.ui.stackedWidget_2.setCurrentIndex(2)

    # ***************
    #     退出登录
    # ***************
    def log_out(self):
        global user_now
        global exit
        exit=True
        self.login = LoginWindow()
        self.close()
        user_now=''


    # ***************
    #     拍照
    # ***************
    def photo(self):
        global frame
        self.photo=frame
        if self.photo!=None:
            self.ui.label_2.setPixmap(frame)
            self.ui.label_2.setScaledContents(True)
