import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex, Qt #Alignment,
from PyQt5.QtGui import QPixmap, QIcon
import os
from my_detect import *

class detectClass(QWidget):
    def __init__(self):
        super().__init__()

        appWidth = 1200
        appHeight = 600
        self.setWindowTitle('YOLOv5 Detection UI')
        self.setGeometry(200, 200, appWidth, appHeight)
        self.setWindowIcon(QIcon(r"E:\Works\Data\etc\1629416.png"))

        
        self.text_weight=QLineEdit(self)
        self.text_source=QLineEdit(self)
        self.text_yolo_dir=QLineEdit(self)
        self.yolo_dir=os.getcwd()
        self.text_yolo_dir.setText(self.yolo_dir)

        self.btn_yolo=QPushButton(self)
        self.btn_yolo.setText("Select YOLO Dir")
        self.btn_yolo.clicked.connect(self.set_yolo_dir)
        self.btn_yolo.setStyleSheet("background-color: #cccccc") #lightgray

        self.btn_source_dir=QPushButton(self)
        self.btn_source_dir.setText("Select Source Dir")
        self.btn_source_dir.clicked.connect(self.set_source_dir)
        self.btn_source_dir.setStyleSheet("background-color: #cccccc")

        self.btn_weight_dir=QPushButton(self)
        self.btn_weight_dir.setText("Select Weight Dir")
        self.btn_weight_dir.clicked.connect(self.set_weight_dir)
        self.btn_weight_dir.setStyleSheet("background-color: #cccccc")


        self.label_notice_save=QLabel(self)
        self.label_notice_save.setText("Threshold (%):")

        self.spinbox_threshold=QSpinBox(self)
        self.spinbox_threshold.setValue(25)
        self.spinbox_threshold.setMinimum(5)
        self.spinbox_threshold.setMaximum(95)
        self.spinbox_threshold.setSingleStep(5)
        self.spinbox_threshold.valueChanged.connect(self.set_threshold)

        '''self.btn_save_txt=QCheckBox(self)
        self.btn_save_txt.setText("save-crop")
        self.btn_save_txt.toggle()
        self.btn_save_txt.stateChanged.connect(self.save_txt)'''

        self.spinbox_cls=QSpinBox(self)
        self.spinbox_cls.setValue(0)
        self.spinbox_cls.setMinimum(0)
        self.spinbox_cls.setMaximum(3)
        self.spinbox_cls.setSingleStep(1)
        self.spinbox_cls.valueChanged.connect(self.set_classes)

        self.btn_detect=QPushButton(self)
        self.btn_detect.setText("detect")
        self.btn_detect.clicked.connect(self.my_detect)
        self.btn_detect.setStyleSheet("background-color: #cccccc")

        

        self.text_notice_save=QLineEdit(self)
        self.text_notice_save.setEnabled(False)


        self.table1=QTableWidget(self)
        self.table1.setStyleSheet("background-color:white; border:1px solid black")
        self.table1.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.column=4
        self.table1.setColumnCount(self.column)
        self.table1.setHorizontalHeaderLabels(["Original Images","Detect", "New Images","Labels"]) #
        self.header=self.table1.horizontalHeader()
        scroll_bar1=self.table1.horizontalScrollBar()
        scroll_bar1.setSingleStep(1)
        for i in range(self.column):
            self.header.setSectionResizeMode(i,QHeaderView.ResizeToContents)

        self.label_img1=QLabel(self)
        self.label_img1.setText("Select Images.")
        self.label_img1.setStyleSheet("background-color:white")
        self.label_img1.setAlignment(Qt.AlignCenter)

        self.label_img2=QLabel(self)
        self.label_img2.setText("Select Images.")
        self.label_img2.setStyleSheet("background-color:white")
        self.label_img2.setAlignment(Qt.AlignCenter)

        self.label_report=QLabel(self)
        self.label_report.setText("report")
        self.label_report.setStyleSheet("background-color:white")
        self.label_report.setAlignment(Qt.AlignCenter)
        
        scroll_report=QScrollArea()
        self.text_report=QLabel(self)
        self.text_report.setStyleSheet("background-color:white")
        #self.text_report.setWordWrap(True)
        scroll_report.setWidget(self.text_report)
        scroll_report.setWidgetResizable(True)
        #scroll_bar=scroll_report.horizontalScrollBar()
        #scroll_bar.setSingleStep(1)

        main_window=QGridLayout()
        window_left=QGridLayout()
        window_right_top=QGridLayout()
        window_right_bottom=QGridLayout()
        window_right=QGridLayout()


        window_left.addWidget(self.text_yolo_dir,1,0,1,3)
        window_left.addWidget(self.btn_yolo,1,3,1,2)
        window_left.addWidget(self.text_weight,2,0,1,3)
        window_left.addWidget(self.btn_weight_dir,2,3,1,2)
        window_left.addWidget(self.text_source,3,0,1,3)
        window_left.addWidget(self.btn_source_dir,3,3,1,2)

        window_left.addWidget(self.label_notice_save,4,0,1,2)
        window_left.addWidget(self.spinbox_threshold,4,2,1,1)
        #window_left.addWidget(self.btn_save_txt,4,3,1,2)
        window_left.addWidget(self.spinbox_cls,4,3,1,2)

        window_left.addWidget(self.text_notice_save,5,0,1,3)
        window_left.addWidget(self.btn_detect,5,3,1,2)
        window_left.addWidget(self.table1, 6,0, 10,5)

        window_right_top.addWidget(self.label_img1, 0,0)
        window_right_top.addWidget(self.label_img2, 0,1)

        window_right_bottom.addWidget(self.label_report, 0,0,1,1)
        window_right_bottom.addWidget(scroll_report, 1,0,5,10)

        window_right.addLayout(window_right_top, 0,0,3,1)
        window_right.addLayout(window_right_bottom, 3,0,1,1)

        main_window.addLayout(window_left, 0,0, 1,1)
        main_window.addLayout(window_right, 0,1, 1,4)   ######(1,1) => left window resize x

        self.setLayout(main_window)

        self.img_ext = ["jpg", "gif", "bmp", "tif", "png"]

        self.table1.itemClicked.connect(self.click_ele)

        self.cmd1=[r'my_detect.py', '--weights','','--source','','--conf-thres','0.10',"--classes", "0", "--iou-thres","0.99","--max-det","1",'--save-txt','--save-crop'] #,'--save-conf', '--save-crop'    #"--classes", "",
        self.cmd2=self.cmd1[:]
        self.my_save_path=""


    def resizeEvent(self, event) : #override
        self.width=self.frameGeometry().width()
        self.height=self.frameGeometry().height()
        #print(self.width, self.height)

    def set_yolo_dir(self):
        dir_path=QFileDialog.getExistingDirectory(self,"Select YOLO Directory")

        if dir_path!="":
            self.yolo_dir=dir_path
            self.text_yolo_dir.setText(dir_path)

    def set_weight_dir(self):
        dir_path=QFileDialog.getOpenFileName(self,"Select Weight File", filter="*.pt")
        if dir_path!=('', ''):
            self.weight_dir,_=dir_path #('E:/Works/YOLO/0414best.pt', '*.pt') <class 'tuple'>
            self.text_weight.setText(self.weight_dir)
            self.cmd2[2]=self.weight_dir
        
    def set_source_dir(self):
        dir_path=QFileDialog.getExistingDirectory(self,"Select Source Directory")
        if dir_path!="":
            self.source_dir=dir_path
            self.text_source.setText(dir_path)

            list2=[]

            if os.path.exists(dir_path):
                for ext in self.img_ext:
                    for file in os.listdir(dir_path):
                        if file.endswith(ext) or file.endswith(ext.upper()):
                            list2.append(file)

            self.row=len(list2)
            self.table1.setRowCount(self.row)
            
            list2.sort()
            for i in range(self.row):
                self.table1.setItem(i,0, QTableWidgetItem(list2[i]))

            self.list1=list2
            self.cmd2[4]=self.source_dir

            self.text_notice_save.setText("")
    
    def set_threshold(self):
        threshold=round(self.spinbox_threshold.value()/100,2)
        self.cmd2[6]=str(threshold)

    def set_classes(self):
        cls=self.spinbox_cls.value()
        self.cmd2[8]=str(cls)
        
    def click_ele(self):

        index_ele=self.table1.selectedIndexes()

        current_row=index_ele[0].row()

        self.show_table_img(current_row, 0)

        if self.text_notice_save.text():
            self.show_table_img(current_row, 2)

    def show_table_img(self, current_row, column):

        if column==0:
            dir=self.source_dir
            img_box=self.label_img1
        elif column==2:
            dir=self.save_dir
            img_box=self.label_img2
        else:
            pass

        img1=self.table1.item(current_row, column)
        img1=os.path.join(dir,img1.text())
        self.pixmap1=QPixmap(img1)
        self.set_image(self.pixmap1, img_box)

    def set_image(self, img, img_box):
        if img.width()==0:
            pass
        else:
            img=img.scaled(img_box.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        img_box.setPixmap(img)

    def save_txt(self,state):
        if state==Qt.Checked:
            self.cmd2.append('--save-crop')
        else:
            if '--save-crop' in self.cmd1:
                self.cmd2.remove('--save-crop')
            else:
                pass

    def my_detect(self):

        self.text_report.setText("")
        self.text_notice_save.setEnabled(False)

        if self.text_yolo_dir.text() and self.text_weight.text() and self.text_source.text():
            dir=self.yolo_dir
            os.chdir(dir)
            
            #print(self.cmd2)
            
            sys.argv=self.cmd2
            opt = parse_opt()
            #self.text_report.setText(launch_msg)
            detect_result_list, self.save_dir, my_logger, conf_list, img_name=main(opt)
            self.my_save_path=os.path.join(self.yolo_dir, self.save_dir)
            #print(conf_list)
            

            for i in range(self.row):
                self.table1.setItem(i,1, QTableWidgetItem(str(detect_result_list[i]))) 
                self.table1.setItem(i,2, QTableWidgetItem(img_name[i])) #new_img_list => save_dir + img_name
                self.table1.setItem(i,3, QTableWidgetItem(str(conf_list[i])))

            append_log=""
            for log in my_logger:
                append_log+=log+"\n"
            self.text_report.setText(append_log)
            

            #self.label_notice_save.setText("Result saved in:")
            self.text_notice_save.setText(self.my_save_path)
            self.text_notice_save.setEnabled(True)

            save_txt_path=os.path.join(self.save_dir,"label_result.csv")
            f1=open(save_txt_path,"w",encoding="utf-8")

            #sum,total_i=0,0
            for i,conf in enumerate(conf_list):# [ [camera 0.95], [scan 0.80] ]
                img_name1=img_name[i]
                f1.write(img_name1+",")
                for label_score in conf: # [camera 0.95]
                    label_split=label_score.split()
                    for index,ele in enumerate(label_split):
                        f1.write(ele+",")
                        '''if index%2==1:
                            sum+=float(ele)
                            total_i+=1'''
                f1.write("\n")

            #print("\nsum: "+str(round(sum,2))+" total_i: "+str(total_i))

            try:
                #f1.write("\nAverage Score: "+str(round(sum/total_i,2))+" sum: "+str(round(sum,2))+" total_i: "+str(total_i))
                f1.write("\nWeight file: "+opt.weight+"\n Source: "+opt.source)
                
            except:
                pass
            f1.close()

        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win1 = detectClass()
    win1.show()
    app.exec_()




