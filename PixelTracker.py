
from PySide.QtGui import *
from PySide.QtCore import *
import cv2
import numpy as np
import sys
import os
import random
from math import sin, cos, radians, pi

from ui_tracker import Ui_mainWindow

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cv_ref_pos = None
        self.ref_color = None
        self.q = None
        self.salient_desc = None
        self.frame = np.zeros((30,60,3), np.uint8)
        self.test_circle_center = (10, 10)
        self.test_circle_dir = 30
        self.test_circle_speed = 4
        self.setupUi(self)
        self.processing_mode = 0
        self.assignWidgets()
        self.show()
        # initialize the AKAZE descriptor
        self.detector = cv2.AKAZE_create(threshold=0.01)  # Detector response threshold to accept point
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        self.setup_camera()

        save_dir = os.path.join(os.path.dirname(__file__), 'frames')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        self.frame_counter = 0

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
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        # initialize the AKAZE descriptor, then detect keypoints
        detector = cv2.AKAZE_create(threshold=0.01)  # Detector response threshold to accept point
        # extract local invariant descriptors from the image
        kps, descs = detector.detectAndCompute(gray_frame, None)
        # the bigger is the response of a point, the more salient is the point
        biggest_response, c = 0, 0
        for m in kps:
            if m.response > biggest_response:
                biggest_response = m.response
                salient_inx = c
            c += 1

        #self.salient_xy = kps[salient_inx].pt
        self.salient_desc = np.zeros((1, 61), dtype='uint8')
        self.salient_desc[0,:] = descs[salient_inx]

    def was_clicked(self , event):
        if not self.processing_mode:
            self.cv_ref_pos = (event.pos().y(),event.pos().x())
            string = "coordinates are =" + str(self.cv_ref_pos[0]) + "," + str(self.cv_ref_pos[1])
            self.goText.append(string)
            r, g, b = self.frame[self.cv_ref_pos]
            self.ref_color = (r.item(), g.item(), b.item())

    def mousePressEvent(self, QMouseEvent):
        #print mouse position
        print(QMouseEvent.pos()) 

    def setup_camera(self):
        # Initialize camera.
        
        self.capture = cv2.VideoCapture(0)
        _, frame = self.capture.read()
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame.shape[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame.shape[1])

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.get_write_image)
        self.timer2.start(1000)


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
        overlay = frame.copy()
        self.test_circle_center = self.move_circle()
        cv2.circle(overlay, self.test_circle_center, 30, (0,0,255), -1)
        cv2.addWeighted(overlay, 0.6, frame, 1 - 0.6, 0, frame)

        self.frame = frame.copy()
        # track the selected pixel
        self.track()

        # Draw a circle at q and repaint QLabel widget
        if self.q != None:
           cv2.circle(frame, self.q, 10, (0, 255, 0), 2)

        image = QImage(frame, frame.shape[1], frame.shape[0], 
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))
        self.image_label.setFixedSize(image.size())
        self.image_label.setAlignment(Qt.AlignLeft)
        
    # Captures a single image from the camera and returns it in PIL format
    def get_write_image(self):
        _, frame = self.capture.read()
        cv2.imwrite("frames/frame_" + str(self.frame_counter) + ".jpg", frame)
        self.frame_counter += 1
     

    def track(self):
        if not self.processing_mode:
            if self.cv_ref_pos != None:
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
        else:
            if self.salient_desc != None:
                gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
                # detect keypoints; very slow!
                kps, descs = self.detector.detectAndCompute(gray_frame, None)
                # Match the features agaist eachother; find 2 match since the first one is the same point
                matches = self.bf.knnMatch(descs, self.salient_desc, k=1)
                matches = [val for sublist in matches for val in sublist]
                # Sort them in the order of their distance. The smallest distance corresponds to the best match
                matches.sort(key=lambda x: x.distance)
                self.q = (int(kps[matches[0].queryIdx].pt[0]), int(kps[matches[0].queryIdx].pt[1]))

    def move_circle(self):
        theta_rad = pi/2 - radians(self.test_circle_dir)
        x = int(self.test_circle_center[0] + self.test_circle_speed*cos(theta_rad))
        y = int(self.test_circle_center[1] + self.test_circle_speed*sin(theta_rad))
        if x>self.frame.shape[1]-1 or y>self.frame.shape[0]-1 or x<0 or y<0:
            self.test_circle_dir =  random.randint(0,360)
            x,y = self.move_circle()
        return x, y

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )
