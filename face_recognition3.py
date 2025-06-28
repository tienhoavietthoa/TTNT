import os
import numpy as np
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import PIL.ImageOps
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime
from time import strftime

import sys

value_from_home = None
def new_tcid(value):
    global value_from_home
    value_from_home = value

# ==== Style constants for cafe theme ====
CAFE_PRIMARY = "#6f4e37"   # Dark brown
CAFE_SECONDARY = "#c7b299" # Light brown/cream
CAFE_BG = "#eee5de"        # Café background
CAFE_ACCENT = "#b4845c"    # Accent brown
CAFE_WHITE = "#f9f6f2"
CAFE_TITLE = "#3e2723"
CAFE_SUCCESS = "#8d8741"
CAFE_DANGER = "#a0522d"

CAFE_FONT = ("Segoe UI", 12)
CAFE_FONT_BOLD = ("Segoe UI", 13, "bold")
CAFE_FONT_TITLE = ("Montserrat", 20, "bold")

def rounded_frame(parent, bg, border_color, corner=20, **kwargs):
    # Helper for custom rounded frame (simulate with canvas)
    f = Frame(parent, bg=bg, **kwargs)
    return f

class Face_Recognition:
    panel=None
    camara=cv2.VideoCapture(0)
    btnOpen=None
    btnClose = None

    check=1
    camara.set(3, 800)
    camara.set(4, 580)
    camara.set(10, 150)

    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("NHẬN DIỆN KHUÔN MẶT")
        self.root.configure(bg=CAFE_BG)
        self.isClicked=False
        self.teacherid = None

        # Cafe style background
        bg_canvas = Canvas(self.root, width=1530, height=790, bg=CAFE_BG, highlightthickness=0)
        bg_canvas.place(x=0, y=0)
        bg_canvas.create_rectangle(0, 0, 1530, 790, fill=CAFE_BG, outline="")

        # Header
        heading = Label(self.root, text="Hệ thống nhận diện khuôn mặt", font=CAFE_FONT_TITLE, bg=CAFE_PRIMARY,
                        fg=CAFE_WHITE, bd=0, relief=FLAT)
        heading.place(x=400, y=20, width=650, height=56)
        heading.config(borderwidth=0, highlightthickness=0)

        self.current_image = None

        print(value_from_home)
        self.teacher_id=value_from_home
        self.lessonid=None

        today = strftime("%d/%m/%Y")
        subject_array = []

        # ===== LEFT FRAME =====
        Left_frame = Frame(self.root, bd=0, bg=CAFE_SECONDARY, highlightbackground=CAFE_PRIMARY,
                           highlightcolor=CAFE_PRIMARY, highlightthickness=2)
        Left_frame.place(x=80, y=70, width=820, height=640)
        Left_frame.configure(borderwidth=0)

        # Panel with rounded border (simulate)
        self.panel = Label(Left_frame, bg=CAFE_BG, borderwidth=0, relief="flat")
        self.panel.place(x=16, y=70, width=788, height=480)

        # Choose lesson
        self.choose_frame = Frame(Left_frame, bg=CAFE_ACCENT, bd=0)
        self.choose_frame.place(x=16, y=10, width=788, height=50)
        choose_label = Label(self.choose_frame, text="Chọn buổi học", bg=CAFE_ACCENT, fg=CAFE_WHITE, font=CAFE_FONT_BOLD)
        choose_label.pack(side=LEFT, padx=16, pady=8)

        # Camera buttons
        self.btnOpen = Button(self.root, text="MỞ CAMERA", font=CAFE_FONT_BOLD, bg=CAFE_SUCCESS, fg=CAFE_WHITE, borderwidth=0,
                              activebackground=CAFE_PRIMARY, activeforeground=CAFE_WHITE, cursor="hand2",
                              command=self.face_recog)
        self.btnOpen.place(x=80, y=720, width=350, height=45)

        self.btnClose = Button(self.root, text="TẮT CAMERA", font=CAFE_FONT_BOLD, bg=CAFE_DANGER, fg=CAFE_WHITE, borderwidth=0,
                               activebackground=CAFE_PRIMARY, activeforeground=CAFE_WHITE, cursor="hand2",
                               command=self.is_clicked)
        self.btnClose.place(x=550, y=720, width=350, height=45)

        # ===== RIGHT FRAME =====
        self.Right_frame = Frame(self.root, bd=0, bg=CAFE_SECONDARY, highlightbackground=CAFE_PRIMARY,
                                 highlightcolor=CAFE_PRIMARY, highlightthickness=2)
        self.Right_frame.place(x=1000, y=70, width=420, height=450)

        self.img_right = PIL.Image.open(r"ImageFaceDetect\unknow.jpg")
        self.img_right = self.img_right.resize((190, 190),PIL.Image.ANTIALIAS)
        self.photoimg_left = ImageTk.PhotoImage(self.img_right)

        self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg=CAFE_BG, borderwidth=0, relief="flat")
        self.f_lbl.place(x=115, y=18, width=190, height=190)

        # Rounded info card
        self.studentID_atten_info=Frame(self.Right_frame, bg=CAFE_WHITE)
        self.studentID_atten_info.place(x=16, y=230, width=388, height=180)

        # IDSV
        self.studentID_label = Label(self.studentID_atten_info, text="ID Sinh Viên:", font=CAFE_FONT_BOLD, bg=CAFE_WHITE, fg=CAFE_PRIMARY)
        self.studentID_label.grid(row=0, column=0, padx=10,pady=10, sticky=W)
        self.studentID_atten_label = Label(self.studentID_atten_info, text="", font=CAFE_FONT, bg=CAFE_WHITE, fg=CAFE_TITLE)
        self.studentID_atten_label.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # TenSV
        self.studentname_label = Label(self.studentID_atten_info, text="Tên Sinh Viên:", font=CAFE_FONT_BOLD, bg=CAFE_WHITE, fg=CAFE_PRIMARY)
        self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.studentname_atten_label = Label(self.studentID_atten_info, text="", font=CAFE_FONT, bg=CAFE_WHITE, fg=CAFE_TITLE)
        self.studentname_atten_label.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Time
        self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:", font=CAFE_FONT_BOLD, bg=CAFE_WHITE, fg=CAFE_PRIMARY)
        self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.studentclass_atten_label = Label(self.studentID_atten_info, text="", font=CAFE_FONT, bg=CAFE_WHITE, fg=CAFE_TITLE)
        self.studentclass_atten_label.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #======================Class-info==============================






    def is_clicked(self):
        self.isClicked=True
        # self.lesson_combo['state'] = "readonly"
        # self.type_combo['state']="readonly"
        # self.notify_label[
        #     'text'] = "Vui lòng chọn ID Buổi học/Tên môn học để nhận diện"
        # self.notify_label['fg']="red"

        print("Camera is Closed")

    def on_closing(self):
        self.isClicked = True
        self.root.destroy()

    def callbackFunc(self,event):
        mls = event.widget.get()
        # print(mls)

        if self.selectsub.get()=="":
            self.btnOpen['state'] = "disabled"
        else:
            c = str(mls).split("-")
            self.lessonid=str(c[1])
            self.subject_name=str(c[0])
            print(self.subject_name)
            self.btnOpen['state']="normal"
            conn = mysql.connector.connect(host='localhost', user='root', password='',
                                           database='face_recognizer', port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select Time_start,Time_end,Class from lesson,subject where `subject`.Subject_id=lesson.Subject_id and Lesson_id=%s ",
                              (self.lessonid,))
            getInfo=my_cursor.fetchone()
            timeclass=str(getInfo[0])+" - "+str(getInfo[1])
            class_name=getInfo[2]
            subles=self.subject_name+" / "+self.lessonid
            self.className_atten_label['text']=class_name
            self.subject_lesson_atten_label['text']=subles
            self.classtime_atten_label['text']=timeclass
        # print(self.lessonid)


    #===========attendance===================
    def mark_attendance(self,i,r,n,d,face_cropped):
        img_id=0

        while True:# khi camera mở lên không có lỗi
            #Them data len csdl
                                now = datetime.now()
                                d1 = strftime("%d/%m/%Y")
                                dtString = now.strftime("%H:%M:%S")
                                ma="SV"+str(i)+d1
                                masp=ma.replace("/","")
                                # print(masp)
                                img_id+=1





                                cv2.imwrite("DiemDanhImage\ " + masp + ".jpg",
                                           face_cropped)
                                #=============================Check_attendance===============================

                                self.img_right = PIL.Image.open(r"DiemDanhImage\ " + masp + ".jpg")
                                self.img_right = self.img_right.resize((190, 190),PIL.Image.ANTIALIAS)
                                self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white", borderwidth=1,
                                                   relief="groove")
                                self.f_lbl.place(x=110, y=10, width=190, height=190)

                                # stdID
                                self.studentID_label = Label(self.studentID_atten_info, text="ID Sinh Viên:",
                                                             font=("times new roman", 13, "bold"), bg="white")
                                self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                   font=("times new roman", 13, "bold"),
                                                                   bg="white", relief="sunken", width=20, justify="left")
                                self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                # name
                                self.studentname_label = Label(self.studentID_atten_info, text="Tên Sinh Viên:",
                                                               font=("times new roman", 13, "bold"),
                                                               bg="white")
                                self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                     font=("times new roman", 13, "bold"), relief="sunken",
                                                                     width=18,
                                                                     bg="white", justify="left")
                                self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                # class
                                self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                font=("times new roman", 13, "bold"),
                                                                bg="white")
                                self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                      font=("times new roman", 13, "bold"),
                                                                      bg="white", relief="sunken", width=20, justify="left")
                                self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)

                            # messagebox.showinfo("Thành công", "Thêm thông tin sinh viên thành công", parent=self.root)




                                if img_id==1:
                                    break

    def face_recog(self):
        self.isClicked = False

        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))
                # Cat anh
                face_cropped = gray_image[y:y + h + 35, x:x + w + 35]
                face_cropped = cv2.cvtColor(face_cropped, cv2.COLOR_GRAY2BGR)
                face_cropped = cv2.resize(face_cropped, (190, 190))
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                               port='3306')
                my_cursor = conn.cursor()
                my_cursor.execute("select Name from student where Student_id=" + str(id))
                n = my_cursor.fetchone()
                if n is not None and isinstance(n, (list, tuple)):
                    n = "+".join(n)
                else:
                    # Xử lý trường hợp khi n là None hoặc không thể lặp lại
                    # Ví dụ:
                    n = "Không xác định"
                my_cursor.execute("select Roll from student where Student_id=" + str(id))
                r = my_cursor.fetchone()
                if r is not None and isinstance(r, (list, tuple)):
                    r = "+".join(map(str, r))
                else:
                    # Xử lý trường hợp khi r là None hoặc không thể lặp lại
                    # Ví dụ:
                    r = "Không xác định"
                my_cursor.execute("select Class from student where Student_id=" + str(id))
                d = my_cursor.fetchone()
                if d is not None and isinstance(d, (list, tuple)):
                    d = "+".join(map(str, d))
                else:
                    # Xử lý trường hợp khi d là None hoặc không thể lặp lại
                    # Ví dụ:
                    d = "Không xác định"

                my_cursor.execute("select Student_id from student where Student_id=" + str(id))
                i = my_cursor.fetchone()
                if i is not None and isinstance(i, (list, tuple)):
                    i = i[0]  # Accessing the first element if it exists
                else:
                    # Handle the case where i is None or not iterable
                    i = "Unknown"

                # Continue processing using the value of i
                if confidence > 85:
                    cv2.putText(img, f"ID:{i}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Name:{n}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    # cv2.imwrite("DiemDanhImage\ " + i + "." + n + '.' + d + ".jpg",
                    #            array[0])
                    self.mark_attendance(i, r, n, d, face_cropped)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknow Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                coord = [x, y, w, h]
            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        self.camara = cv2.VideoCapture(0)
        self.camara.set(3, 800)  ##chiều dài
        self.camara.set(4, 580)  ##chiều rộng
        self.camara.set(10, 150)  # độ sáng

        while True:
            ret, img = self.camara.read()
            img = recognize(img, clf, faceCascade)
            # Resize the image to fit the panel size
            img = cv2.resize(img, (800, 480))
            # Convert the image to RGB format
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Convert the image to PIL format
            img = PIL.Image.fromarray(img)
            # Convert the PIL image to Tkinter PhotoImage
            img = PIL.ImageTk.PhotoImage(image=img)
            # Update the panel with the new image
            self.panel.configure(image=img)
            self.panel.image = img  # Keep a reference
            self.panel.update()

            if self.isClicked:  ##Bam Q de thoat cam
                break

        self.camara.release()
        cv2.destroyAllWindows()


if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Face_Recognition(root)
    root.mainloop()# cua so hien len

