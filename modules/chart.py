from PyQt5.QtWidgets import *
import pyqtgraph as pg
import psycopg2
from ui import *
class chart_ui(QMainWindow):
    type='OpenCircle'
    def __init__(self):
        super().__init__()
        self.ui=Ui_chartWindow()
        self.ui.setupUi(self)
        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.makeChart(self.ui.horizontalLayout_10,'cathode')
        self.makeChart(self.ui.horizontalLayout_11,'anode')
        self.makeChart(self.ui.horizontalLayout_12,'mouth')
        self.makeChart(self.ui.horizontalLayout_13,'year')

    def makeChart(self,layout,time):
        sqlname=f'{time}{self.type}'
        # 添加示例数据到图表容器
        x = []
        y = []
        self.chartContainer = pg.PlotWidget()
        layout.addWidget(self.chartContainer)
        conn = psycopg2.connect(database='DataMy', user='postgres', password='123', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute(f"select * from {sqlname} order by id ASC")
        rows = cur.fetchall()
        for row in rows:
           x.append(row[0])
           y.append(row[1])
        conn.commit()
        conn.close()

        self.chartContainer.setBackground('w')
        self.chartContainer.plot(x, y, pen='k')
        self.chartContainer.setTitle(type)
