import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex, Qt #Alignment,
from PyQt5.QtGui import QPixmap, QIcon
import os
from my_detect import *

class detectClass(QWidget):
    def __init__(self):
        super().__init__()

        appWidth = 1500
        appHeight = 800
        self.setWindowTitle('YOLOv5 Detection UI')
        self.setGeometry(100, 100, appWidth, appHeight)
        self.setWindowIcon(QIcon(r"E:\Works\Data\etc\image.png"))

        
        self.text_weight=QLineEdit(self)
        self.text_source=QLineEdit(self)
        self.text_yolo_dir=QLineEdit(self)
        self.yolo_dir=os.getcwd()
        self.text_yolo_dir.setText(self.yolo_dir)

        self.btn_yolo=QPushButton(self)
        self.btn_yolo.setText("Select YOLO Dir")
        self.btn_yolo.clicked.connect(self.set_yolo_dir)
        self.btn_yolo.setStyleSheet("background-color: #cccccc")

        self.btn_source_dir=QPushButton(self)
        self.btn_source_dir.setText("Select Source Dir")
        self.btn_source_dir.clicked.connect(self.set_source_dir)
        self.btn_source_dir.setStyleSheet("background-color: #cccccc")

        self.btn_weight_dir=QPushButton(self)
        self.btn_weight_dir.setText("Select Weight Dir")
        self.btn_weight_dir.clicked.connect(self.set_weight_dir)
        self.btn_weight_dir.setStyleSheet("background-color: #cccccc")




        #show details
        self.btn_details_toggle=QPushButton("set details")
        self.btn_details_toggle.clicked.connect(self.toggle_details)
        self.set_details_group=QGroupBox("setting parameters")
        self.set_details_group.setVisible(False)

        #parameters
        #CONF threshold
        self.label_threshold=QLabel(self)
        self.label_threshold.setText("Threshold (%):")

        self.spinbox_threshold=QSpinBox(self)
        self.spinbox_threshold.setValue(25)
        self.spinbox_threshold.setMinimum(5)
        self.spinbox_threshold.setMaximum(95)
        self.spinbox_threshold.setSingleStep(5)
        self.spinbox_threshold.valueChanged.connect(self.set_threshold)

        # IOU threshold
        self.label_iou=QLabel(self)
        self.label_iou.setText("IOU (%):")

        self.spinbox_iou=QSpinBox(self)
        self.spinbox_iou.setValue(45)
        self.spinbox_iou.setMinimum(5)
        self.spinbox_iou.setMaximum(95)
        self.spinbox_iou.setSingleStep(5)
        self.spinbox_iou.valueChanged.connect(self.set_iou)

        #max-det
        self.label_max_det=QLabel(self)
        self.label_max_det.setText("max-det:")

        self.spinbox_max_det=QSpinBox(self)
        self.spinbox_max_det.setValue(5)
        self.spinbox_max_det.setMinimum(1)
        self.spinbox_max_det.setMaximum(100)
        self.spinbox_max_det.setSingleStep(1)
        self.spinbox_max_det.valueChanged.connect(self.set_max_det)

        #
        self.btn_save_txt=QCheckBox(self)
        self.btn_save_txt.setText("save-txt")
        self.btn_save_txt.toggle()
        self.btn_save_txt.stateChanged.connect(self.save_txt)

        self.btn_save_crop=QCheckBox(self)
        self.btn_save_crop.setText("save-crop")
        self.btn_save_crop.toggle()
        self.btn_save_crop.stateChanged.connect(self.save_crop)

        self.btn_save_conf=QCheckBox(self)
        self.btn_save_conf.setText("save-conf")
        #self.btn_save_conf.toggle()
        self.btn_save_conf.setChecked(False)
        self.btn_save_conf.stateChanged.connect(self.save_conf)

        self.btn_no_save=QCheckBox(self)
        self.btn_no_save.setText("no-save")
        #self.btn_no_save.toggle()
        self.btn_save_conf.setChecked(False)
        self.btn_no_save.stateChanged.connect(self.no_save)

        '''self.spinbox_cls=QSpinBox(self)
        self.spinbox_cls.setValue(0)
        self.spinbox_cls.setMinimum(0)
        self.spinbox_cls.setMaximum(3)
        self.spinbox_cls.setSingleStep(1)
        self.spinbox_cls.valueChanged.connect(self.set_classes)'''

        self.btn_detect=QPushButton(self)
        self.btn_detect.setText("detect")
        self.btn_detect.clicked.connect(self.my_detect)
        self.btn_detect.setStyleSheet("background-color: #cccccc")


        self.text_save_dir=QLineEdit(self)
        self.text_save_dir.setEnabled(False)


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


        
        details_layout = QGridLayout()

        details_layout.addWidget(self.label_threshold)
        details_layout.addWidget(self.spinbox_threshold)
        details_layout.addWidget(self.label_iou)
        details_layout.addWidget(self.spinbox_iou)
        details_layout.addWidget(self.label_max_det)
        details_layout.addWidget(self.spinbox_max_det)
        details_layout.addWidget(self.btn_save_txt)
        details_layout.addWidget(self.btn_save_crop)
        details_layout.addWidget(self.btn_save_conf)
        details_layout.addWidget(self.btn_no_save)

        self.set_details_group.setLayout(details_layout)


        #MAIN_layout

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
        
        '''window_left.addWidget(self.label_threshold,4,0,1,2)
        window_left.addWidget(self.spinbox_threshold,4,2,1,1)
        window_left.addWidget(self.btn_save_txt,4,3,1,2)
        window_left.addWidget(self.btn_save_conf,5,0,1,2)
        window_left.addWidget(self.btn_save_crop,5,3,1,2)'''
        #window_left.addWidget(self.spinbox_cls,4,3,1,2)


        window_left.addWidget(self.btn_details_toggle,4,0,1,5)
        window_left.addWidget(self.set_details_group,5,0,1,5)


        window_left.addWidget(self.text_save_dir,6,0,1,3)
        window_left.addWidget(self.btn_detect,6,3,1,2)
        window_left.addWidget(self.table1, 7,0, 10,5)

        window_right_top.addWidget(self.label_img1, 0,0)
        window_right_top.addWidget(self.label_img2, 0,1)

        window_right_bottom.addWidget(self.label_report, 0,0,1,1)
        window_right_bottom.addWidget(scroll_report, 1,0,5,10)

        window_right.addLayout(window_right_top, 0,0,3,1)
        window_right.addLayout(window_right_bottom, 3,0,1,1)

        main_window.addLayout(window_left, 0,0, 1,1)
        main_window.addLayout(window_right, 0,1, 1,4)   ######(1,1) => left window resize x

        self.setLayout(main_window)

        self.img_ext = ["jpg", "gif", "bmp", "tif", "png","jpeg"]

        self.table1.itemClicked.connect(self.click_ele)

        self.cmd1=[r'my_detect.py', '--weights','','--source','','--conf-thres','0.25',"--iou-thres","0.45", "--max-det","5", '--save-txt','--save-crop'] #,'--save-conf'   #"--classes", "",,'--nosave'
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

            self.table1.clearContents()
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

            #self.text_save_dir.setText("")

    def toggle_details(self):
        self.set_details_group.setVisible(not self.set_details_group.isVisible())
    
    def set_threshold(self):
        threshold=round(self.spinbox_threshold.value()/100,2)
        self.cmd2[6]=str(threshold)

    '''def set_classes(self):
        cls=self.spinbox_cls.value()
        self.cmd2[8]=str(cls)'''
    
    def set_iou(self):
        iou=round(self.spinbox_iou.value()/100,2)
        self.cmd2[8]=str(iou)
    
    def set_max_det(self):
        max_det=self.spinbox_max_det.value()
        self.cmd2[10]=str(max_det)

    
    def click_ele(self):

        index_ele=self.table1.selectedIndexes()

        current_row=index_ele[0].row()

        self.show_table_img(current_row, 0)

        if self.text_save_dir.text():
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
            self.cmd2.append('--save-txt')
        else:
            if '--save-txt' in self.cmd2:
                self.cmd2.remove('--save-txt')
            else:
                pass

    def save_conf(self,state):
        if state==Qt.Checked:
            self.cmd2.append('--save-conf')
        else:
            if '--save-conf' in self.cmd2:
                self.cmd2.remove('--save-conf')
            else:
                pass
    
    def save_crop(self,state):
        if state==Qt.Checked:
            self.cmd2.append('--save-crop')
        else:
            if '--save-crop' in self.cmd2:
                self.cmd2.remove('--save-crop')
            else:
                pass

    def no_save(self,state):
        if state==Qt.Checked:
            self.cmd2.append('--nosave')
        else:
            if '--nosave' in self.cmd2:
                self.cmd2.remove('--nosave')
            else:
                pass

    def add_param(self,state, param1):
        if state==Qt.Checked:
            self.cmd2.append(param1)
        else:
            if param1 in self.cmd2:
                self.cmd2.remove(param1)
            else:
                pass
    
    def my_detect(self):

        if self.text_yolo_dir.text() and self.text_weight.text() and self.text_source.text():
            dir=self.yolo_dir
            os.chdir(dir)

            self.text_report.setText(".")
            self.text_save_dir.setEnabled(False)
            self.text_save_dir.setText(".")
            
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
            

            #self.label_threshold.setText("Result saved in:")
            self.text_save_dir.setText(self.my_save_path)
            self.text_save_dir.setEnabled(True)

            save_txt_path=os.path.join(self.save_dir,"label_result.csv")
            f1=open(save_txt_path,"w",encoding="utf-8")

            #sum,total_i=0,0
            class_list=[]
            for i,conf in enumerate(conf_list):# [ [camera 0.95], [scan 0.80] ]
                img_name1=img_name[i]
                f1.write(img_name1+",")
                for label_score in conf: # [camera 0.95]
                    label_split=label_score.split()
                    for index,ele in enumerate(label_split):
                        f1.write(ele+",")
                        '''if index%2==0:
                            sum+=float(ele)
                            total_i+=1'''
                        if index%2==0:
                            class_list.append(ele)
                            
                f1.write("\n")
            f1.write("\n")
            
            class_list_set=set(class_list)
            for cls in class_list_set:
                num_cls=class_list.count(cls)

                try:
                    num_cls_rate=round(num_cls/len(class_list),4)*100
                    f1.write(cls+","+str(num_cls)+","+str(num_cls_rate)+"%\n")
                except:
                    print("len(class_list) is 0")

            #print("\nsum: "+str(round(sum,2))+" total_i: "+str(total_i))

            try:
                #f1.write("\nAverage Score: "+str(round(sum/total_i,2))+" sum: "+str(round(sum,2))+" total_i: "+str(total_i))
                f1.write("\nWeight file: "+self.cmd2[2]+"\nSource: "+self.cmd2[4])
                
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




