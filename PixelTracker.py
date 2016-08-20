
from PySide.QtGui import *
from PySide.QtCore import *
import cv2
import numpy as np
import sys

from ui_tracker import Ui_mainWindow

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cv_ref_pos = (-1, -1)
        self.ref_color = (None, None, None)
        self.q = (-1, -1)
        self.video_size = QSize(100, 200)
        self.frame = np.zeros((self.video_size.height(),self.video_size.width(),3), np.uint8)
        self.setupUi(self)
        self.processing_mode = 0
        self.assignWidgets()
        self.show()
        self.setup_camera()

    def assignWidgets(self):
        self.mode_1.clicked.connect(self.method_1)
        self.mode_2.clicked.connect(self.method_2)
        self.image_label.mousePressEvent = self.was_clicked
    

    def method_1(self):
        self.processing_mode = 0
        self.goText.append("method_1!")

    def method_2(self):
        self.processing_mode = 1
        self.goText.append("method_2!")

    def was_clicked(self , event):
        if not self.processing_mode:
            self.cv_ref_pos = (event.pos().y(),event.pos().x())
        else:
            self.cv_ref_pos = (event.pos().y(),event.pos().x())

        string = "coordinates are =" + str(self.cv_ref_pos[0]) + "," + str(self.cv_ref_pos[1])
        self.goText.append(string)
        r, g, b = self.frame[self.cv_ref_pos]
        self.ref_color = (r.item(),g.item(),b.item())

        self.goText.append(str(self.ref_color))



    def mousePressEvent(self, QMouseEvent):
        #print mouse position
        print(QMouseEvent.pos()) 

    def setup_camera(self):
        # Initialize camera.
        
        self.capture = cv2.VideoCapture(0)
        _, frame = self.capture.read()
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        # Read frame from camera and repaint QLabel widget.

        _, frame = self.capture.read()

        frame_Lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        L,a,b = cv2.split(frame_Lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        L = clahe.apply(L)
        frame_Lab = cv2.merge([L,a,b])
        frame = cv2.cvtColor(frame_Lab, cv2.COLOR_Lab2RGB)

        frame = cv2.flip(frame, 1)

        # add a testing region
        cv2.circle(frame, (200,100), 10, (0,0,255), -1)

        self.frame = frame.copy()
        # track the selected pixel
        self.track()

        # Draw a circle at q and repaint QLabel widget
        if self.q[0] != -1:
           cv2.circle(frame, self.q, 10, (0, 255, 0), 2)

        image = QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))
        self.image_label.setFixedSize(image.size())
        self.image_label.setAlignment(Qt.AlignLeft)
        
    def track(self):
        if self.cv_ref_pos[0] != -1:
           # Split image into channels
            rs, gs, bs = cv2.split(self.frame)
            # Find absolute differences for each channel
            diff_r =  cv2.absdiff(rs, self.ref_color[0])
            diff_g =  cv2.absdiff(gs, self.ref_color[1])
            diff_b =  cv2.absdiff(bs, self.ref_color[2])
           # Calculate L1 distance
            dist = cv2.add(diff_r, diff_g)
            dist = cv2.add(dist, diff_b)
            # Find the location of pixel with minimum color distance
            _, _, min_loc, _ = cv2.minMaxLoc(dist)
            # keep the q
            self.q = min_loc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
