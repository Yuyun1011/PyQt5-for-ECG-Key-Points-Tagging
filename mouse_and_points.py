import sys
import numpy as np
import pickle
# from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QGridLayout, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint


class ScatterPlotWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.P_exist_bool = False
        self.T_exist_bool = False
        self.A_exist_bool = False
        self.R_GT_list = []
        self.P_GT_list = []
        self.T_GT_list = []
        self.mouse_mode = 0
        self.data = data
        self.initUI()

    def initUI(self):
        # 创建文本框
        self.noise_level_txt = QTextBrowser(self)
        self.noise_level_txt.resize(200, 23)
        self.noise_level_txt.move(1100, 50)

        self.P_exist_txt = QTextBrowser(self)
        self.P_exist_txt.resize(50, 23)
        self.P_exist_txt.move(1550, 50)
        self.P_exist_txt.setText('No')

        self.T_exist_txt = QTextBrowser(self)
        self.T_exist_txt.resize(50, 23)
        self.T_exist_txt.move(1750, 50)
        self.T_exist_txt.setText('No')

        self.A_exist_txt = QTextBrowser(self)
        self.A_exist_txt.resize(50, 23)
        self.A_exist_txt.move(2000, 50)
        self.A_exist_txt.setText('No')

        # RPT标注按钮
        btnR = QPushButton('Mode_R Yellow', self)
        btnR.move(100, 50)

        btnP = QPushButton('Mode_P Cyan', self)
        btnP.move(200, 50)

        btnT = QPushButton('Mode_T Green', self)
        btnT.move(300, 50)

        btnK = QPushButton('Kill RPT', self)
        btnK.move(400, 50)

        # 噪声程度按钮
        btnN100 = QPushButton('N100', self)
        btnN100.move(600, 50)

        btnN70 = QPushButton('N70', self)
        btnN70.move(700, 50)

        btnN40 = QPushButton('N40', self)
        btnN40.move(800, 50)

        btnN10 = QPushButton('N10', self)
        btnN10.move(900, 50)

        btnN0 = QPushButton('N0', self)
        btnN0.move(1000, 50)

        # P、T波存在判定按钮
        btnPExist = QPushButton('P Exist', self)
        btnPExist.move(1450, 50)

        btnTExist = QPushButton('T Exist', self)
        btnTExist.move(1650, 50)

        # 心率失常存在判定
        btnArrhythmia = QPushButton('Arrhythmia Exist', self)
        btnArrhythmia.move(1880, 50)

        # Connect buttons to event handlers
        btnR.clicked.connect(self.onButtonRClicked)
        btnP.clicked.connect(self.onButtonPClicked)
        btnT.clicked.connect(self.onButtonTClicked)
        btnK.clicked.connect(self.onButtonKClicked)

        btnN100.clicked.connect(self.onButtonN100Clicked)
        btnN70.clicked.connect(self.onButtonN70Clicked)
        btnN40.clicked.connect(self.onButtonN40Clicked)
        btnN10.clicked.connect(self.onButtonN10Clicked)
        btnN0.clicked.connect(self.onButtonN0Clicked)

        btnPExist.clicked.connect(self.onButtonPExistClicked)
        btnTExist.clicked.connect(self.onButtonTExistClicked)

        btnArrhythmia.clicked.connect(self.onButtonArrhythmiaClicked)

        # Set window properties
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Three Buttons Example')
        self.show()
        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

    def onButtonRClicked(self):
        self.mouse_mode = 'R'
    
    def onButtonPClicked(self):
        self.mouse_mode = 'P'

    def onButtonTClicked(self):
        self.mouse_mode = 'T'
    
    def onButtonKClicked(self):
        self.mouse_mode = 0

    def onButtonN100Clicked(self):
        self.noise_level_txt.setText('纯噪声')
        # print(' ')

    def onButtonN70Clicked(self):
        self.noise_level_txt.setText('30%以上清晰的R-Peak')

    def onButtonN40Clicked(self):
        self.noise_level_txt.setText('60%以上清晰的R-Peak')

    def onButtonN10Clicked(self):
        self.noise_level_txt.setText('几乎全部为清晰的R-Peak')
    
    def onButtonN0Clicked(self):
        self.noise_level_txt.setText('清晰的R-Peak和PT波')

    def onButtonPExistClicked(self):
        if self.P_exist_bool == False:
            self.P_exist_txt.setText('Yes')
            self.P_exist_bool = True
        else:
            self.P_exist_txt.setText('No')
            self.P_exist_bool = False

    def onButtonTExistClicked(self):
        if self.T_exist_bool == False:
            self.T_exist_txt.setText('Yes')
            self.T_exist_bool = True
        else:
            self.T_exist_txt.setText('No')
            self.T_exist_bool = False

    def onButtonArrhythmiaClicked(self):
        if self.A_exist_bool == False:
            self.A_exist_txt.setText('Yes')
            self.A_exist_bool = True
        else:
            self.A_exist_txt.setText('No')
            self.A_exist_bool = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制坐标轴
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(50, self.height() - 50, self.width() - 50, self.height() - 50)
        painter.drawLine(50, self.height() - 50, 50, 50)

        # 绘制数据点
        brush = QBrush(Qt.SolidPattern)
        for point in self.data:
            # print(point['highlighted'])
            if point['highlighted'] == 1:
                brush.setColor(Qt.red)
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(point['x'], point['y']), 5, 5)
            elif point['highlighted'] == 0:
                brush.setColor(Qt.blue)
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(point['x'], point['y']), 2, 2)
            elif point['highlighted'] == 'R':
                brush.setColor(Qt.yellow)
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(point['x'], point['y']), 5, 5)
            elif point['highlighted'] == 'P':
                brush.setColor(Qt.cyan)
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(point['x'], point['y']), 5, 5)
            elif point['highlighted'] == 'T':
                brush.setColor(Qt.green)
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(point['x'], point['y']), 5, 5)

        # 绘制连线
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        for i in range(len(self.data) - 1):
            p1 = QPoint(self.data[i]['x'], self.data[i]['y'])
            p2 = QPoint(self.data[i + 1]['x'], self.data[i + 1]['y'])
            painter.drawLine(p1, p2)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

        # print(x)

        # 判断鼠标是否在某个数据点附近
        for point in self.data:
            if abs(point['x'] - x) <= 10 and abs(point['y'] - y) <= 10 and point['highlighted'] == 0:
                point['highlighted'] = 1
            elif point['highlighted'] == 0 or point['highlighted'] == 1:
                point['highlighted'] = 0

        # for point_index in range(len(self.data)):
        #     if abs(self.data[point_index]['x'] - x) <= 10 and abs(self.data[point_index]['y'] - y) <= 10:
        #         self.data[point_index]['highlighted'] = True
        #     else:
        #         self.data[point_index]['highlighted'] = False

        self.update()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        a_clicked_points_list = []
        if event.button() == Qt.LeftButton:
            for point in self.data:
                if abs(point['x'] - x) <= 10 and abs(point['y'] - y) <= 10:
                    point['highlighted'] = self.mouse_mode
                    # if self.mouse_mode == 'R' or self.mouse_mode == 0:
                    a_clicked_points_list.append(self.data.index(point))
            if len(a_clicked_points_list) != 0:
                if self.mouse_mode == 'R' and a_clicked_points_list not in self.R_GT_list:
                    self.R_GT_list.append(a_clicked_points_list)
                elif self.mouse_mode == 'P' and a_clicked_points_list not in self.P_GT_list:
                    self.P_GT_list.append(a_clicked_points_list)
                elif self.mouse_mode == 'T' and a_clicked_points_list not in self.T_GT_list:
                    self.T_GT_list.append(a_clicked_points_list)
                elif self.mouse_mode == 0:
                    self.remove_points(self.R_GT_list, a_clicked_points_list)
                    self.remove_points(self.P_GT_list, a_clicked_points_list)
                    self.remove_points(self.T_GT_list, a_clicked_points_list)
            print(self.T_GT_list)
    
    def remove_points(self, GT_list, removing_points_list):
        removing_temp_list = []
        for a_GT_list in GT_list:
            for a_point_GT_list in a_GT_list:
                if a_point_GT_list in removing_points_list:
                    GT_list.remove(a_GT_list)
                    break

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('折线散点图')
        self.setGeometry(100, 100, 600, 600)
        # self.scatter_plot_widget = ScatterPlotWidget([
        #     {'x': 100, 'y': 100, 'highlighted': False},
        #     {'x': 200, 'y': 300, 'highlighted': False},
        #     {'x': 300, 'y': 200, 'highlighted': False},
        #     {'x': 400, 'y': 400, 'highlighted': False},
        # ])
        self.scatter_plot_widget = ScatterPlotWidget(data)
        self.setCentralWidget(self.scatter_plot_widget)
        # self.setMouseTracking(False)

def create_many_points():
    point_list = []
    for index in range(3600):
        one_point = {'x': index, 'y': index, 'highlighted': False}
        point_list.append(one_point)
    return point_list

def create_sin_points():
    point_list = []
    time = np.arange(0, 3600, 4)
    sin_wave = 100*np.sin(time/20) + 300
    for index in range(900):
        one_point = {'x': time[index], 'y': sin_wave[index], 'highlighted': False}
        point_list.append(one_point)
    return point_list
    
def ecg_data_loader(data_path):
    ecg_signal = []
    point_list = []
    with open(data_path, 'rb') as f:
        data = pickle.load(f)
        ecg_signal = data[0]
    for index in range(0, 3600, 1):
        one_point = {'x': index/1.5 + 100, 'y': -ecg_signal[index]*500 + 800, 'highlighted': 0}
        point_list.append(one_point)
    return point_list


if __name__ == '__main__':
    data_path = 'dataset/sample_1.pkl'
    # data = create_many_points()
    # data = create_sin_points()
    data = ecg_data_loader(data_path)

    app = QApplication(sys.argv)
    window = MainWindow(data)
    window.show()
    sys.exit(app.exec_())
