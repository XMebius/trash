import sys
import os
import cv2
from servo import PCA9685
import csv
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer,pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel, QListView,QPushButton
from PyQt5.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import record #, ultraSonic
kinds=[0,0,0,0,0]#total four kitchen others recycle harmful
names=["kitchen","others","recycle","harmful"]
distance=[[111,111,111,111],[222,222,222,222],[333,333,333,333],[444,444,444,444]]
count=0
stage=0
class VideoPlayerThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cap = cv2.VideoCapture(self.video_path)
                continue

            # Convert the OpenCV frame to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.frame_signal.emit(q_img)

class CSVReaderThread(QThread):
    csv_data_signal = pyqtSignal(list)

    def __init__(self, csv_file_path):
        super().__init__()
        self.csv_file_path = csv_file_path

    def run(self):
        global count
        global kinds
        global stage
        global distance
        csv_data = []

        with open("/home/mebius/workspace/yolov5/expression.csv", 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                csv_data.append(row)
        self.csv_data_signal.emit(csv_data)
                ####舵机驱动
        
        if stage==0:
            first_column_data = []
            #print("jin qu le")
            time.sleep(2)
            #print("aaa")
            with open("/home/mebius/workspace/yolov5/results.csv", 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                #print("aaaaaa")
                header_skipped = False  # 用于跳过标题行的标志
                for row in csv_reader:
                    if not header_skipped:
                        header_skipped =True
                        continue  # 跳过标题行
                    if row:  # 确保行不为空
                        first_column_data.append(float(row[0]))  # 读取第一列的数据并转换为整数
            if first_column_data:
                print("First column data:", first_column_data[0])
                if(first_column_data[0]==0.0 or first_column_data[0]==1.0 or first_column_data[0]==3.0):
                    print("我是可回收")
                    angle=-90
                    pca.setServoAngle(channel=1, angle=30)#zheng dao
                    pca.setServoAngle(channel=0, angle=angle)#zheng dao
                    print("shuchule")
                    time.sleep(1)
                    pca.setServoAngle(channel=1, angle=0)#zheng da
                    time.sleep(1)
                    pca.setServoAngle(channel=1, angle=40)
                    pca.setServoAngle(channel=0, angle=50)
                    kinds=record.writeCsv(first_column_data[0],kinds)

                    # pca.setServoAngle(channel=0, angle=90)
                    # time.sleep(1)
                elif(first_column_data[0]==5.0 or first_column_data[0]==6.0 or first_column_data[0]==9.0):
                    print("我是有害垃圾")
                    angle=-30
                    pca.setServoAngle(channel=1, angle=30)#zheng dao
                    pca.setServoAngle(channel=0, angle=angle)#zheng dao
                    time.sleep(1)
                    pca.setServoAngle(channel=1, angle=0)#zheng da
                    time.sleep(2)
                    pca.setServoAngle(channel=1, angle=40)
                    pca.setServoAngle(channel=0, angle=50)
                    kinds=record.writeCsv(first_column_data[0],kinds)
                elif(first_column_data[0]==4.0 or first_column_data[0]==10.0 or first_column_data[0]==11.0):
                    print("我是厨余")
                    angle=30
                    # per_servo=int((angle-now_servo)/5)
                    # for i in range(5):
                    #    i=i+1
                    #    pca.setServoAngle(channel=0, angle=now_servo+i*per_servo)#ke hui shou
                    #    time.sleep(0.2)
                    # pca.setServoAngle(channel=1, angle=100)#zheng dao
                    # time.sleep(1)
                    pca.setServoAngle(channel=1, angle=30)#zheng dao
                    pca.setServoAngle(channel=0, angle=angle)#zheng dao
                    time.sleep(1)
                    pca.setServoAngle(channel=1, angle=0)#zheng da
                    time.sleep(2)
                    pca.setServoAngle(channel=1, angle=40)
                    pca.setServoAngle(channel=0, angle=50)
                    kinds=record.writeCsv(first_column_data[0],kinds)
                elif(first_column_data[0]==2.0 or first_column_data[0]==8.0 or first_column_data[0]==7.0):
                    print("我是其他")
                    angle=90
                    # now_servo=pca.getCurrentServoAngle(channel=0)
                    # per_servo=int((angle-now_servo)/5)
                    # for i in range(5):
                    #    i=i+1
                    #    pca.setServoAngle(channel=0, angle=now_servo+i*per_servo)#ke hui shou
                    #    time.sleep(0.2)
                    # pca.setServoAngle(channel=1, angle=100)#zheng dao
                    pca.setServoAngle(channel=1, angle=30)#zheng dao
                    pca.setServoAngle(channel=0, angle=angle)#zheng dao
                    time.sleep(1)
                    pca.setServoAngle(channel=1, angle=0)#zheng da
                    time.sleep(2)
                    pca.setServoAngle(channel=1, angle=40)
                    pca.setServoAngle(channel=0, angle=50)
                    kinds=record.writeCsv(first_column_data[0],kinds)
            time.sleep(2)
        if stage==1:
            first_column_data = []
            time.sleep(1.5) 
            with open("/home/mebius/workspace/yolov5/results.csv", 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                #print("aaaaaa")
                header_skipped = False  # 用于跳过标题行的标志
                for row in csv_reader:
                    if not header_skipped:
                        header_skipped = True
                        continue  # 跳过标题行
                    if row:  # 确保行不为空
                        first_column_data.append(float(row[0]))  # 读取第一列的数据并转换为整数
            if first_column_data:
                #这里是复赛的机械臂代码
                pass

class ExternalScriptThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Preparing for detecting")
        command = "cd /home/mebius/workspace/yolov5/ && python detect.py && cd /home/mebius/workspace/code/ && python ultrasonic.py"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"{result.stdout}")
        print(f"{result.stderr}")
        print("Start detecing")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, csv_file_path, callback):
        super().__init__()
        self.csv_file_path = csv_file_path
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.csv_file_path:
            self.callback()

class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("视频播放器")
        self.setGeometry(100, 100, 680, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.csv_list_view = QListView(self)
        self.layout.addWidget(self.csv_list_view)
        self.csv_model = QStandardItemModel(self.csv_list_view)
        self.csv_list_view.setModel(self.csv_model)

        self.csv_thread = None

        self.start_csv_reader()

        self.video_thread = None
        self.run_external_script()


        # 创建一个定时器，定期检查CSV文件的更改
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_csv_changes)
        self.timer.start(100)  # 每秒检查一次

        
        # 创建文件变化监视器
        self.file_change_handler = FileChangeHandler(self.csv_file_path, self.update_csv_data)
        self.file_observer = Observer()
        self.file_observer.schedule(self.file_change_handler, path=os.path.dirname(self.csv_file_path))
        self.file_observer.start()

    def start_video(self):
        if self.video_thread is None or not self.video_thread.isRunning():
            self.video_thread = VideoPlayerThread("/home/mebius/workspace/code/video.mp4")
            self.video_thread.frame_signal.connect(self.update_video_frame)
            self.video_thread.start()

    def update_video_frame(self, q_img):
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)

    def start_csv_reader(self):
        self.csv_file_path = "/home/mebius/workspace/yolov5/results.csv"
        if self.csv_thread is None or not self.csv_thread.isRunning():
            self.csv_thread = CSVReaderThread(self.csv_file_path)
            self.csv_thread.csv_data_signal.connect(self.update_csv_list)
            self.csv_thread.start()
    @pyqtSlot(list)
    def update_csv_list(self, csv_data):
        self.csv_model.clear() 
        for row in csv_data:
            item = QStandardItem(" | ".join(row))
            self.csv_model.appendRow(item)

    def check_csv_changes(self):
        # 在定时器中检查CSV文件的更改
        if os.path.exists(self.csv_file_path):
            modification_time = os.path.getmtime(self.csv_file_path)
            current_time = time.time()
            if current_time - modification_time > 1.0:  # 文件在1秒内被修改
                
                self.update_csv_data()

    def update_csv_data(self):
        # 当CSV文件发生更改时，更新UI中的数据
        self.start_csv_reader()
        
    def run_external_script(self):
        self.external_script_thread = ExternalScriptThread()
        self.external_script_thread.start()

if __name__ == '__main__':

    pca = PCA9685(address=0x40, debug=True)

    pca.setPWMFreq(50)
    pca.setServoAngle(channel=1, angle=30)#zheng dao
    pca.setServoAngle(channel=0, angle=0)#zheng dao
    with open("/home/mebius/workspace/yolov5/results.csv", 'w', newline='') as csv_file:
        pass
    with open("/home/mebius/workspace/yolov5/expression.csv", 'w', newline='') as csv_file:
        pass
    app = QApplication(sys.argv)
    window = VideoPlayerApp()
    window.show()
    window.start_video()
    sys.exit(app.exec_())
