import os
import random
import numpy as np
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import PIL.Image
import mysql.connector
from tkcalendar import DateEntry
from time import strftime
import cv2

mydata = []

# Cafe style palette
CAFE_PRIMARY = "#6f4e37"   # Dark brown
CAFE_SECONDARY = "#c7b299" # Light brown/cream
CAFE_BG = "#eee5de"        # Café background
CAFE_ACCENT = "#b4845c"    # Accent brown
CAFE_WHITE = "#f9f6f2"
CAFE_TITLE = "#3e2723"
CAFE_SUCCESS = "#8d8741"
CAFE_DANGER = "#a0522d"
CAFE_BUTTON = "#faca6e"
CAFE_BUTTON_TEXT = "#82591a"

CAFE_FONT = ("Segoe UI", 12)
CAFE_FONT_BOLD = ("Segoe UI", 13, "bold")
CAFE_FONT_TITLE = ("Montserrat", 24, "bold")

class Student:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Quản lý sinh viên")
        self.root.configure(bg=CAFE_BG)
        today = strftime("%d-%m-%Y")

        # ======================variables================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_class = StringVar()
        self.var_nameclass = StringVar()

        # BG color
        bg_canvas = Canvas(self.root, width=1530, height=790, bg=CAFE_BG, highlightthickness=0)
        bg_canvas.place(x=0, y=0)
        bg_canvas.create_rectangle(0, 0, 1530, 790, fill=CAFE_BG, outline="")

        # Header
        heading = Label(self.root, text="Thông tin", font=CAFE_FONT_TITLE, bg=CAFE_PRIMARY, fg=CAFE_WHITE, bd=0, relief=FLAT)
        heading.place(x=400, y=22, width=700, height=54)

        # Time & Date section
        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)
        lbl = Label(self.root, font=("Segoe UI", 13, "bold"), bg=CAFE_WHITE, fg=CAFE_PRIMARY)
        lbl.place(x=80, y=35, width=100, height=20)
        time()
        lbl1 = Label(self.root, text=today, font=("Segoe UI", 13, "bold"), bg=CAFE_WHITE, fg=CAFE_PRIMARY)
        lbl1.place(x=80, y=60, width=100, height=20)

        # Main frame
        main_frame = Frame(self.root, bd=0, bg=CAFE_BG)
        main_frame.place(x=23, y=102, width=1482, height=671)

        # ====LEFT (Student info)====
        self.getNextid()
        Left_frame = Frame(main_frame, bd=0, bg=CAFE_SECONDARY, highlightbackground=CAFE_PRIMARY, highlightthickness=2)
        Left_frame.place(x=10, y=10, width=730, height=646)

        label_Update_att = Label(Left_frame, bg=CAFE_ACCENT, fg=CAFE_WHITE, text="Thông tin sinh viên", font=("Segoe UI", 16, "bold"))
        label_Update_att.place(x=0, y=1, width=720, height=44)

        # Course info
        current_course_frame = LabelFrame(Left_frame, bd=0, bg=CAFE_BG, fg=CAFE_TITLE, text="Thông tin khoá học", font=("Segoe UI", 12, "bold"), highlightbackground=CAFE_PRIMARY, highlightthickness=1)
        current_course_frame.place(x=8, y=55, width=710, height=110)

        dep_label = Label(current_course_frame, text="Chuyên ngành", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        dep_label.grid(row=0, column=0, padx=10, sticky=W)
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=CAFE_FONT, state="readonly", width=20)
        dep_combo["values"] = ("Chọn chuyên ngành", "Điện tử viễn thông", "IT", "Cơ khí", "Điện", "Kế toán", "Tự động hóa")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=8, sticky=W)

        course_label = Label(current_course_frame, text="Hệ đào tạo", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        course_label.grid(row=0, column=2, padx=10, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=CAFE_FONT, state="readonly", width=20)
        course_combo["values"] = ("Chọn hệ", "Chính quy", "Liên Thông", "CLC")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=8, sticky=W)

        year_label = Label(current_course_frame, text="Năm học", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        year_label.grid(row=1, column=0, padx=10, sticky=W)
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=CAFE_FONT, state="readonly", width=20)
        year_combo["values"] = ("Chọn năm học", "2020-21", "2021-22", "2022-23", "2023-24")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=8, sticky=W)

        semester_label = Label(current_course_frame, text="Học kì", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        semester_label.grid(row=1, column=2, padx=10, sticky=W)
        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=CAFE_FONT, state="readonly", width=20)
        semester_combo["values"] = ("Chọn học kì", "Học kì I", "Học kì II")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=8, sticky=W)

        # Class & Student info
        class_student_frame = LabelFrame(Left_frame, bd=0, bg=CAFE_BG, fg=CAFE_TITLE, text="Thông tin lớp học", font=CAFE_FONT_BOLD, highlightbackground=CAFE_PRIMARY, highlightthickness=1)
        class_student_frame.place(x=8, y=170, width=710, height=410)

        # Student ID
        studentID_label = Label(class_student_frame, text="ID Sinh Viên:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        studentID_label.grid(row=0, column=0, padx=12, pady=6, sticky=W)
        studentID_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_std_id, font=CAFE_FONT, state="disabled")
        studentID_entry.grid(row=0, column=1, padx=10, pady=6, sticky=W)
        studentName_label = Label(class_student_frame, text="Tên Sinh Viên:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        studentName_label.grid(row=0, column=2, padx=10, pady=6, sticky=W)
        studentName_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_std_name, font=CAFE_FONT)
        studentName_entry.grid(row=0, column=3, padx=10, pady=6, sticky=W)

        # Class
        class_div_label = Label(class_student_frame, text="Lớp học:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        class_div_label.grid(row=1, column=0, padx=12, pady=6, sticky=W)
        class_div_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_div, font=CAFE_FONT)
        class_div_entry.grid(row=1, column=1, padx=10, pady=6, sticky=W)
        roll_no_label = Label(class_student_frame, text="CMND", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        roll_no_label.grid(row=1, column=2, padx=10, pady=6, sticky=W)
        roll_no_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_roll, font=CAFE_FONT)
        roll_no_entry.grid(row=1, column=3, padx=10, pady=6, sticky=W)

        # Gender
        gender_label = Label(class_student_frame, text="Giới tính:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        gender_label.grid(row=2, column=0, padx=12, pady=6, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, font=CAFE_FONT, state="readonly", width=18)
        gender_combo["values"] = ("Nam", "Nữ", "Khác")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=6, sticky=W)
        dob_label = Label(class_student_frame, text="Ngày sinh:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        dob_label.grid(row=2, column=2, padx=10, pady=6, sticky=W)
        self.dob_entry = DateEntry(class_student_frame, width=18, bd=2, selectmode='day', year=2021, month=5, font=CAFE_FONT, day=22, date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=2, column=3, padx=10, pady=6, sticky=W)

        # Email, Phone, Address
        email_label = Label(class_student_frame, text="Email:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        email_label.grid(row=3, column=0, padx=12, pady=6, sticky=W)
        email_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_email, font=CAFE_FONT)
        email_entry.grid(row=3, column=1, padx=10, pady=6, sticky=W)
        phone_label = Label(class_student_frame, text="SĐT:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        phone_label.grid(row=3, column=2, padx=10, pady=6, sticky=W)
        phone_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_phone, font=CAFE_FONT)
        phone_entry.grid(row=3, column=3, padx=10, pady=6, sticky=W)
        address_label = Label(class_student_frame, text="Địa chỉ:", font=CAFE_FONT_BOLD, bg=CAFE_BG, fg=CAFE_TITLE)
        address_label.grid(row=4, column=0, padx=12, pady=6, sticky=W)
        address_entry = ttk.Entry(class_student_frame, width=20, textvariable=self.var_address, font=CAFE_FONT)
        address_entry.grid(row=4, column=1, padx=10, pady=6, sticky=W)

        # Photo radio
        self.var_radio1 = StringVar()
        radionbtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Có ảnh", value="Yes")
        radionbtn1.grid(row=6, column=0, pady=4)
        radionbtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Không ảnh", value="No")
        radionbtn2.grid(row=6, column=1, pady=4)

        # Button frame
        btn_frame = Frame(class_student_frame, bg=CAFE_BG)
        btn_frame.place(x=0, y=270, width=705, height=38)
        save_btn = Button(btn_frame, text="Save", command=self.add_data, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=14)
        save_btn.grid(row=0, column=0, padx=6)
        update_btn = Button(btn_frame, text="Edit", command=self.update_data, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=14)
        update_btn.grid(row=0, column=1, padx=6)
        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=14)
        delete_btn.grid(row=0, column=2, padx=6)
        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=14)
        reset_btn.grid(row=0, column=3, padx=6)

        btn_frame1 = Frame(class_student_frame, bg=CAFE_BG)
        btn_frame1.place(x=0, y=315, width=705, height=38)
        take_photo_btn = Button(btn_frame1, text="Lấy ảnh sinh viên", command=self.generate_dataset, font=CAFE_FONT_BOLD, bg=CAFE_SUCCESS, fg=CAFE_WHITE, width=28)
        take_photo_btn.grid(row=0, column=0, padx=6)
        update_photo_btn = Button(btn_frame1, text="Training Data", command=self.train_classifier, font=CAFE_FONT_BOLD, bg=CAFE_ACCENT, fg=CAFE_WHITE, width=28)
        update_photo_btn.grid(row=0, column=1, padx=6)

        # ====RIGHT (Student Table/Search)====
        Right_frame = Frame(main_frame, bd=0, bg=CAFE_SECONDARY, highlightbackground=CAFE_PRIMARY, highlightthickness=2)
        Right_frame.place(x=750, y=10, width=720, height=330)

        # Search frame
        search_frame = Frame(Right_frame, bg=CAFE_ACCENT)
        search_frame.place(x=7, y=7, width=705, height=56)
        self.var_com_search = StringVar()
        search_label = Label(search_frame, text="Tìm kiếm theo :", font=CAFE_FONT_BOLD, bg=CAFE_ACCENT, fg=CAFE_WHITE)
        search_label.grid(row=0, column=0, padx=12, pady=8, sticky=W)
        search_combo = ttk.Combobox(search_frame, font=CAFE_FONT, state="readonly", width=13, textvariable=self.var_com_search)
        search_combo["values"] = ("ID Sinh viên", "Tên sinh viên", "Lớp biên chế")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=4, pady=8, sticky=W)
        self.var_search = StringVar()
        search_entry = ttk.Entry(search_frame, width=15, font=CAFE_FONT, textvariable=self.var_search)
        search_entry.grid(row=0, column=2, padx=10, pady=8, sticky=W)
        search_btn = Button(search_frame, text="Search", font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10, command=self.search_data)
        search_btn.grid(row=0, column=3, padx=4)
        showAll_btn = Button(search_frame, text="ALL", font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10, command=self.fetch_data)
        showAll_btn.grid(row=0, column=4, padx=4)

        # Table frame
        table_frame = Frame(Right_frame, bg=CAFE_BG)
        table_frame.place(x=7, y=72, width=703, height=240)
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        self.student_table = ttk.Treeview(table_frame, column=("id","dep","course","year","sem","name","div","roll","gender","dob","email","phone","address","photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        for name, text in [
            ("id", "ID Sinh viên"), ("dep", "Chuyên ngành"), ("course", "Chương trình học"), ("year", "Năm học"), ("sem", "Học kì"),
            ("name", "Họ tên"), ("div", "Lớp biên chế"), ("roll", "CMND"), ("gender", "Giới tính"), ("dob", "Ngày sinh"),
            ("email", "Email"), ("phone", "Số điện thoại"), ("address", "Địa chỉ"), ("photo", "Trạng thái ảnh")
        ]:
            self.student_table.heading(name, text=text)
            self.student_table.column(name, width=110)
        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()
        self.getNextid()

        # ===============BOTTOM RIGHT CLASS====================
        Underright_frame = Frame(main_frame, bg=CAFE_SECONDARY, highlightbackground=CAFE_PRIMARY, highlightthickness=2)
        Underright_frame.place(x=750, y=345, width=720, height=310)
        label_studentsb = Label(Underright_frame, bg=CAFE_ACCENT, fg=CAFE_WHITE, text="Quản lý lớp học", font=CAFE_FONT_BOLD)
        label_studentsb.place(x=0, y=1, width=720, height=36)

        # Search Class
        self.var_com_searchclass = StringVar()
        search_combo = ttk.Combobox(Underright_frame, font=CAFE_FONT, textvariable=self.var_com_searchclass, state="readonly", width=12)
        search_combo["values"] = ("Lớp", "Tên lớp")
        search_combo.current(0)
        search_combo.place(x=20, y=55, width=120)
        self.var_searchclass = StringVar()
        searchstd_entry = ttk.Entry(Underright_frame, textvariable=self.var_searchclass, width=13, font=CAFE_FONT)
        searchstd_entry.place(x=155, y=55, width=140)
        searchstd_btn = Button(Underright_frame, command=self.search_Classdata, text="Search", font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10)
        searchstd_btn.place(x=310, y=53)
        showAllstd_btn = Button(Underright_frame, text="All", command=self.fetch_Classdata, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10)
        showAllstd_btn.place(x=420, y=53)

        # student/class
        studentid_label = Label(Underright_frame, text="Lớp học:", font=CAFE_FONT_BOLD, bg=CAFE_SECONDARY, width=12)
        studentid_label.place(x=20, y=120, width=100)
        studentid_entry = ttk.Entry(Underright_frame, textvariable=self.var_class, font=CAFE_FONT, width=20)
        studentid_entry.place(x=135, y=120, width=200)
        subsub_label = Label(Underright_frame, text="Tên lớp học:", font=CAFE_FONT_BOLD, bg=CAFE_SECONDARY)
        subsub_label.place(x=20, y=165, width=100)
        subsub_entry = ttk.Entry(Underright_frame, width=22, textvariable=self.var_nameclass, font=CAFE_FONT)
        subsub_entry.place(x=135, y=165, width=200)

        # btn_frameteacher
        btn_framestd = Frame(Underright_frame, bg=CAFE_BG)
        btn_framestd.place(x=20, y=245, width=455, height=48)
        addTc_btn = Button(btn_framestd, text="Add", command=self.add_Classdata, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10)
        addTc_btn.grid(row=0, column=0, padx=6, pady=6)
        deleteTc_btn = Button(btn_framestd, text="Delete", command=self.delete_Classdata, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10)
        deleteTc_btn.grid(row=0, column=1, padx=6, pady=6)
        updateTc_btn = Button(btn_framestd, text="Update", command=self.update_Classdata, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10)
        updateTc_btn.grid(row=0, column=2, padx=6, pady=6)
        resetTc_btn = Button(btn_framestd, text="Reset", command=self.reset_Classdata, font=CAFE_FONT_BOLD, bg=CAFE_BUTTON, fg=CAFE_BUTTON_TEXT, width=10)
        resetTc_btn.grid(row=0, column=3, padx=6, pady=6)

        # table_frame
        tablestd_frame = Frame(Underright_frame, bg=CAFE_BG)
        tablestd_frame.place(x=490, y=40, width=200, height=250)
        scroll_x = ttk.Scrollbar(tablestd_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablestd_frame, orient=VERTICAL)
        self.StudentTable = ttk.Treeview(tablestd_frame, column=("class", "name"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.StudentTable.xview)
        scroll_y.config(command=self.StudentTable.yview)
        self.StudentTable.heading("class", text="Lớp học")
        self.StudentTable.heading("name", text="Tên")
        self.StudentTable["show"] = "headings"
        self.StudentTable.column("class", width=80)
        self.StudentTable.column("name", width=80)
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease>", self.get_cursorClass)
        self.fetch_Classdata()

    #============function decration===============
    def slider(self):
        if self.count>=len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text+self.txt[self.count]
            self.heading.config(text=self.text)

        self.count+=1

        self.heading.after(100,self.slider)

    def heading_color(self):
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def getNextid(self):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        my_cursor.execute(
            "SELECT  Student_id from student ORDER BY Student_id DESC limit 1")
        lastid = my_cursor.fetchone()
        if (lastid == None):
            self.var_std_id.set("1")
        else:
            nextid = int(lastid[0]) + 1
            self.var_std_id.set(str(nextid))

        conn.commit()
        conn.close()
        # return  self.var_id
    def add_data(self):
        # ========check class================
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')

        my_cursor = conn.cursor()
        my_cursor.execute("select Class from `class` ")
        ckclass = my_cursor.fetchall()
        arrayClass = []
        for chc in ckclass:
            # print(chc[0])
            arrayClass.append(str(chc[0]))
        if self.var_dep.get()=="Chọn chuyên ngành" or self.var_std_name.get()=="" or self.var_std_id.get()=="" or self.var_div.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif (self.var_div.get() not in arrayClass):
            messagebox.showerror("Error", "Tên lớp học không tồn tại ! Vui lòng kiểm tra lại", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                    self.var_std_id.get(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    # self.var_dob.get(),
                    self.dob_entry.get_date().strftime('%d/%m/%Y'),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_radio1.get()
                ))
                print(conn)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Thành công","Thêm thông tin sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    #=======================fetch-data========================
    def fetch_data(self):
        conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

        my_cursor = conn.cursor()
        my_cursor.execute("Select * from student")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #======================get-cursor==============================
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        self.var_std_id.set(data[0]),
        self.var_dep.set(data[1]),
        self.var_course.set(data[2]),
        self.var_year.set(data[3]),
        self.var_semester.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.dob_entry.set_date(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_radio1.set(data[13]),

    def update_data(self):
        if self.var_dep.get()=="Chọn chuyên ngành" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Bạn có muốn cập nhật thông tin sinh viên này không?",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Class=%s,"
                                      "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",(
                                            self.var_dep.get(),
                                            self.var_course.get(),
                                            self.var_year.get(),
                                            self.var_semester.get(),
                                            self.var_std_name.get(),
                                            self.var_div.get(),
                                            self.var_roll.get(),
                                            self.var_gender.get(),
                                            self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                            self.var_email.get(),
                                            self.var_phone.get(),
                                            self.var_address.get(),
                                            self.var_radio1.get(),
                                            self.var_std_id.get()
                                        ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Thành công","Cập nhật thông tin sinh viên thành công",parent=self.root)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    #Delete Function
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Lỗi","Không được bỏ trống ID sinh viên",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Xoá sinh viên","Bạn có muốn xóa sinh viên này?",parent=self.root)
                if delete>0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        sql="delete from student where Student_id=%s"
                        val=(self.var_std_id.get(),)
                        my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Xóa","Xóa sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)


    #===================Reset function====================
    def reset_data(self):
        self.var_dep.set("Chọn chuyên ngành"),
        self.var_course.set("Chọn hệ"),
        self.var_year.set("Chọn năm học"),
        self.var_semester.set("Chọn học kì"),
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_div.set(""),
        self.var_roll.set(""),
        self.var_gender.set("Nam"),
        self.dob_entry.set_date(strftime("%d/%m/%Y")),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),

        self.var_radio1.set(""),
        self.getNextid()
    def search_data(self):
            if self.var_com_search.get() == "" or self.var_search.get() == "":
                messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ",parent=self.root)

            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                   database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Sinh Viên"
                    if (self.var_com_search.get() == "ID Sinh viên"):
                        self.var_com_search.set("Student_id")
                    elif (self.var_com_search.get() == "Tên sinh viên"):
                        self.var_com_search.set("Name")
                    elif (self.var_com_search.get() == "Lớp biên chế"):
                        self.var_com_search.set("Class")

                    my_cursor.execute("select * from student where " + str(
                        self.var_com_search.get()) + " Like '%" + str(self.var_search.get()) + "%'")
                    data = my_cursor.fetchall()
                    if (len(data) != 0):
                        self.student_table.delete(*self.student_table.get_children())
                        for i in data:
                            self.student_table.insert("", END, values=i)
                        messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",parent=self.root)
                        conn.commit()
                    else:
                        self.student_table.delete(*self.student_table.get_children())
                        messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    #=============generate dataset and take photo=================
    def generate_dataset(self):
        if self.var_dep.get()=="Chọn chuyên ngành" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

                my_cursor = conn.cursor()
                # my_cursor.execute("select * from student")
                # myresult=my_cursor.fetchall()
                id=self.var_std_id.get()
                # for x in myresult:
                #     id+=1
                my_cursor.execute("update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Class=%s,"
                              "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",
                              (
                                  self.var_dep.get(),
                                  self.var_course.get(),
                                  self.var_year.get(),
                                  self.var_semester.get(),
                                  self.var_std_name.get(),
                                  self.var_div.get(),
                                  self.var_roll.get(),
                                  self.var_gender.get(),
                                  self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                  self.var_email.get(),
                                  self.var_phone.get(),
                                  self.var_address.get(),
                                  self.var_radio1.get(),
                                  self.var_std_id.get()
                              ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                #=========load haar===================
                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)
                    #scaling factor 1.3
                    ##minimum neighbor 5
                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]

                        return  face_cropped
                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    net,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        # face=cv2.resize(face_cropped(my_frame),(190,190))
                        face=cv2.cvtColor(face_cropped(my_frame),cv2.COLOR_BGR2GRAY)
                        fill_name_path="data/user."+str(id)+"."+str(img_id)+".jpg"

                        cv2.imwrite(fill_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",face)

                    if cv2.waitKey(1)==13 or int(img_id)==120:#duyet du 120 anh
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Kết quả","Tạo dữ liệu khuôn mặt thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    #==========================TrainDataSet=======================
    def train_classifier(self):
        data_dir=("data")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]
        for image in path:
            img=PIL.Image.open(image).convert('L')
            imageNp=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids=np.array(ids)

        #=================Train data classifier and save============
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Kết quả","Training dataset Completed",parent=self.root)

    # ========================================Function Student======================================

    def get_cursorClass(self, event=""):
            cursor_row = self.StudentTable.focus()
            content = self.StudentTable.item(cursor_row)
            rows = content['values']
            self.var_class.set(rows[0])
            self.var_nameclass.set(rows[1])


    def add_Classdata(self):
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()


            # =========check class=================
            my_cursor.execute("select Class from `class` ")
            ckClass = my_cursor.fetchall()
            arrayClass = []
            for chs in ckClass:
                # print(chs[0])
                arrayClass.append(str(chs[0]))
            conn.commit()
            conn.close()
            if self.var_class.get() == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

            elif (self.var_class.get()  in arrayClass):
                messagebox.showerror("Error", "Class đã tồn tại! Vui lòng kiểm tra lại", parent=self.root)
            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                   database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()
                    my_cursor.execute("insert into class values(%s,%s)", (
                        self.var_class.get(),
                        self.var_nameclass.get(),
                    ))
                    conn.commit()
                    self.fetch_Classdata()
                    self.reset_Classdata()
                    conn.close()
                    messagebox.showinfo("Thành công", "Thêm thông tin lớp học thành công",
                                        parent=self.root)
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def reset_Classdata(self):
            self.var_class.set("")
            self.var_nameclass.set("")

    def fetch_Classdata(self):
            # global mydata
            # mydata.clear()
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("Select * from class")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.StudentTable.delete(*self.StudentTable.get_children())
                for i in data:
                    self.StudentTable.insert("", END, values=i)
                    mydata.append(i)
                conn.commit()
            conn.close()

    def update_Classdata(self):
            if self.var_class == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

            else:
                try:
                    Update = messagebox.askyesno("Update", "Bạn có muốn cập nhật bản ghi này không?", parent=self.root)
                    if Update > 0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                       database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        my_cursor.execute("UPDATE `class` SET Name = %s  WHERE "
                                          "`Class` = %s",
                                          (
                                              self.var_nameclass.get(),
                                              self.var_class.get(),
                                          ))
                    else:
                        if not Update:
                            return
                    messagebox.showinfo("Thành công", "Cập nhật thông tin lớp học thành công",
                                        parent=self.root)
                    conn.commit()
                    self.reset_Classdata()
                    self.fetch_Classdata()
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

            # Delete Function

    def delete_Classdata(self):
            if self.var_class== "" or self.var_nameclass.get() == "":
                messagebox.showerror("Lỗi", "Không được bỏ trống thông tin! ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Xoá bản ghi", "Bạn có muốn xóa bản ghi này ?", parent=self.root)
                    if delete > 0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                       database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        sql = "delete from class where Class=%s "
                        val = (self.var_class.get(),)
                        my_cursor.execute(sql, val)
                    else:
                        if not delete:
                            return
                    conn.commit()
                    # self.fetch_data()p
                    conn.close()
                    messagebox.showinfo("Xóa", "Xóa bản ghi thành công", parent=self.root)
                    self.reset_Classdata()
                    self.fetch_Classdata()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    def search_Classdata(self):
            if self.var_com_searchclass.get() == "" or self.var_searchclass.get() == "":
                messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ",parent=self.root)

            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                   database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Sinh Viên"
                    if (self.var_com_searchclass.get() == "Lớp"):
                        self.var_com_searchclass.set("Class")
                    elif (self.var_com_searchclass.get() == "Tên lớp"):
                        self.var_com_searchclass.set("Name")

                    my_cursor.execute("select * from class where " + str(
                        self.var_com_searchclass.get()) + " Like '%" + str(self.var_searchclass.get()) + "%'")
                    data = my_cursor.fetchall()
                    if (len(data) != 0):
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        for i in data:
                            self.StudentTable.insert("", END, values=i)
                        messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",parent=self.root)
                        conn.commit()
                    else:
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Student(root)
    root.mainloop()# cua so hien len
