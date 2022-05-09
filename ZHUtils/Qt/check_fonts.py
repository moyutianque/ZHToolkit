import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFrame, QLabel, QApplication, QGridLayout, QHBoxLayout
from utils import ExpandingButton, BorderedFrame

class ImageViewer(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setup_ui()

    def setup_ui(self):
        # self.setStyleSheet("background-color: white;")
        # Image container
        self.image_frame = BorderedFrame(self)
        self.image_region = QGridLayout(self.image_frame)
        # self.image_region = QGridLayout()
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap('./icon.png').scaledToHeight(200))
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_region.addWidget(self.image_label)
        self.image_caption = QLabel("[file name] [file description]")
        self.image_caption.setAlignment(QtCore.Qt.AlignCenter)
        self.image_caption.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse) 
        self.image_region.addWidget(self.image_label)

        # Tools
        ## TOOL col 1
        self.image_sec_frame = BorderedFrame(self)
        self.image_section = QGridLayout(self.image_sec_frame)
        text1 = QLabel("图像")
        # text1.setFont(QtGui.QFont("LiSu",weight=QtGui.QFont.Bold))
        text1.setFont(QtGui.QFont("Times New Roman", weight=QtGui.QFont.Bold))
        text1.setAlignment(QtCore.Qt.AlignCenter)
        # self.text1.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.btn_upload = ExpandingButton("上传")
        self.btn_upload.clicked.connect(lambda: self.not_implemented_func()) 
        # btn_upload.clicked.connect(lambda checked, arg=variable_a: self.not_implemented_func(arg)) 
        self.btn_last_img = ExpandingButton("上一张")
        self.btn_last_img.clicked.connect(lambda: self.not_implemented_func()) 
        self.image_section.addWidget(text1, 0,0,1,1)
        self.image_section.addWidget(self.btn_upload, 1,0,1,1)
        self.image_section.addWidget(self.btn_last_img, 3,0,2,1)

        ## Tool col 2
        self.xfqc_frame = BorderedFrame(self)
        self.xfqc = QGridLayout(self.xfqc_frame)
        text2 = QLabel("心房纤颤")
        text2.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        text2.setAlignment(QtCore.Qt.AlignCenter)

        self.xfqc_mid = QHBoxLayout()
        self.xfqc_mid_col1 = QVBoxLayout()
        btn_xfqc_pred = ExpandingButton("预测")
        btn_xfqc_pred.clicked.connect(lambda: self.not_implemented_func()) 
        self.xfqc_mid_col1.addWidget(btn_xfqc_pred)

        self.xfqc_mid_col2 = QVBoxLayout()
        self.btn_xfqc_add = ExpandingButton("添加标记")
        self.btn_xfqc_add.clicked.connect(lambda: self.not_implemented_func()) 
        self.btn_xfqc_del = ExpandingButton("删除标记")
        self.btn_xfqc_del.clicked.connect(lambda: self.not_implemented_func()) 
        self.xfqc_mid_col2.addWidget(self.btn_xfqc_add)
        self.xfqc_mid_col2.addWidget(self.btn_xfqc_del)
        self.xfqc_mid.addLayout(self.xfqc_mid_col1)
        self.xfqc_mid.addLayout(self.xfqc_mid_col2)

        text_xfqc_bot = QLabel("目测平均心室率: ")
        text_xfqc_bot.setAlignment(QtCore.Qt.AlignLeft)

        self.xfqc.addWidget(text2, 0,0,1,5)
        self.xfqc.addLayout(self.xfqc_mid, 1,0,1,5)
        self.xfqc.addWidget(text_xfqc_bot, 2,0,1,2)

        ## Tool col 3
        self.xfpd_frame = BorderedFrame(self)
        self.xfpd = QGridLayout(self.xfpd_frame)
        text3 = QLabel("心房扑动")
        text3.setFont(QtGui.QFont("Times", weight=QtGui.QFont.Bold))
        text3.setAlignment(QtCore.Qt.AlignCenter)

        self.xfpd_ruler1 = ExpandingButton("心房标尺")
        self.xfpd_ruler1.clicked.connect(lambda: self.not_implemented_func())
        self.xfpd_ruler2 = ExpandingButton("心室标尺")
        self.xfpd_ruler2.clicked.connect(lambda: self.not_implemented_func())

        text_xfpd_bot = QLabel("心房下传心室比: ")
        text_xfpd_bot.setAlignment(QtCore.Qt.AlignLeft)

        self.xfpd.addWidget(text3, 0,0,1,5)
        self.xfpd.addWidget(self.xfpd_ruler1, 1,0,1,5)
        self.xfpd.addWidget(self.xfpd_ruler2, 2,0,1,5)
        self.xfpd.addWidget(text_xfpd_bot, 3,0,1,2)
    


        # organize main layout
        self.main_layout = QVBoxLayout(self)  # adding widgets to layot
        self.main_layout.addWidget(self.image_frame)
        self.tool_layout = QHBoxLayout()
        self.tool_layout.addWidget(self.image_sec_frame)
        self.tool_layout.addWidget(self.xfqc_frame)
        self.tool_layout.addWidget(self.xfpd_frame)

        self.main_layout.addLayout(self.tool_layout)
        self.setLayout(self.main_layout)  # set layot

    def not_implemented_func(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    app.exec_()
