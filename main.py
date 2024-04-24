from datetime import datetime
import os.path
import time
import tkinter as tk
import re
import customtkinter
from PIL import Image, ImageTk
import cv2
import util
import pymongo
from CTkMessagebox import CTkMessagebox
import face_recognition
import pickle
import smtplib
from email.message import EmailMessage
import ssl
import vlc
import datetime
import matplotlib.pyplot as plt
from pymongo.errors import  DuplicateKeyError
from tkinter import font
class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title("Face Reconition Based Attendance System")
        self.geometry("950x650")
        self.resizable(False, False)

        # Create frames beforehand
        self.right_frame_for_welcome = customtkinter.CTkFrame(master=self, fg_color="#204B6B", corner_radius=0,
                                                    width=750, height=750)
        self.right_frame_for_welcome.pack_propagate(0)
        self.right_frame_for_welcome.pack(side="right", padx=(1, 0))

        self.Login = customtkinter.CTkFrame(master=self, fg_color="#204B6B", corner_radius=0,
                                            width=750, height=750)
        self.Login.pack_propagate(0)
        self.Login.pack_forget()  # Initially hide the Login frame
        #_______________________________________________________________
        # Initially set the current frame to the Welcome frame (can be adjusted if needed)
        self.current_right_frame = self.right_frame_for_welcome
        #________________________________________________________________
        # Left side view
        self.left_view_for_wel = customtkinter.CTkFrame(master=self, fg_color="#4385b7", corner_radius=0,
                                                        width=200, height=750)
        self.left_view_for_wel.pack_propagate(0)
        self.left_view_for_wel.pack(side="right")
        #________________________________________________________________
        # _____________________Collage view On Left side______________________
        self.canvas3 = customtkinter.CTkFrame(self.left_view_for_wel, width=180, height=200, fg_color="white")
        self.canvas3.pack(side="top", pady=(30, 10))

        image_path = "images/sanskar.jpeg"
        image = Image.open(image_path)
        resized_image = image.resize((180, 212))
        photo = ImageTk.PhotoImage(resized_image)

        self.image_label = customtkinter.CTkLabel(self.canvas3, image=photo,text="")
        self.image_label.pack()
        #_____________________Button Frame_______________________
        self.btns_frame = customtkinter.CTkFrame(master=self.left_view_for_wel, width=220, height=380,
                                                 fg_color="transparent")
        self.btns_frame.pack(side="top", padx=(2, 2), pady=(50, 5), fill="both")

        self.Register_btn = customtkinter.CTkButton(master=self.btns_frame, text="Register", width=200, height=45,
                                                    font=("Arial Bold", 22), hover_color="#B0510C",
                                                    fg_color="#EE6B06", text_color="#fff",
                                                    command=lambda :self.switchFrame(self.Register_btn)
                                                    )
        self.Register_btn.pack(
            side="top", padx=(2, 2), pady=(10, 5), fill="both"
        )

        self.Login_btn = customtkinter.CTkButton(master=self.btns_frame, text="Login", width=190, height=45,
                                                 font=("Arial Bold", 20), hover_color="#B0510C",
                                                 fg_color="#EE6B06", text_color="#fff",
                                                 command=lambda : self.switchFrame(self.Login_btn)
                                                 )
        self.Login_btn.pack(
            side="top", padx=(2, 2), pady=(20, 5), fill="both"
        )

        self.Admin_btn = customtkinter.CTkButton(master=self.btns_frame, text="Admin", width=190, height=45,
                                                 font=("Arial Bold", 20), hover_color="#B0510C",
                                                 fg_color="#EE6B06", text_color="#fff",
                                                 command=lambda :self.switchFrame(self.Admin_btn)
                                                 )
        self.Admin_btn.pack(
            side="top", padx=(2, 2), pady=(20, 5), fill="both"
        )
        #___________________Collage Image On main Window__________________________
        self.canvas4 = customtkinter.CTkFrame(self.right_frame_for_welcome, width=600, height=100, fg_color="white")
        self.canvas4.pack(side="top", pady=(30, 10))

        image_path = "images/clg.jpg"
        image = Image.open(image_path)
        resized_image = image.resize((600, 100))
        photo = ImageTk.PhotoImage(resized_image)

        self.image_label = customtkinter.CTkLabel(self.canvas4, image=photo,text="")
        self.image_label.pack()
        #_______________________Video View On Main Window__________________
        # Initialize VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        # Load video file
        self.media = self.instance.media_new("video/faceRecoAnim.mp4")
        self.player.set_media(self.media)
        # Set up tkinter window
        self.canvas = tk.Canvas(self.right_frame_for_welcome, bg="black", width=640, height=400)
        self.canvas.pack(side="top", pady=(27, 10))
        # Bind VLC player to tkinter canvas
        self.player.set_hwnd(self.canvas.winfo_id())
        self.player.play()
        # initializing the user encoding list
        self.newUserEncoding = []

    def register(self):
        self.register_frame = customtkinter.CTkFrame(master=self, fg_color="#204B6B", corner_radius=0,
                                                              width=750, height=750)
        self.register_frame.pack_propagate(0)
        self.register_frame.pack(side="right", padx=(1, 0))

        ########### Credential Label______________________
        self.credential = customtkinter.CTkLabel(master=self.register_frame, text="Credential",
                                                 font=("Arial Black", 25),
                                                 text_color="#fff").pack(
            anchor="nw", pady=(29, 0), padx=27)

        ############ Name Label__________________________
        self.name_label = customtkinter.CTkLabel(master=self.register_frame, text="Name",
                                                 font=("Arial Bold", 17),
                                                 text_color="#fff").pack(anchor="nw",
                                                                         pady=(25, 0),
                                                                         padx=27)
        ########### Name Entry Feild
        self.stu_name = customtkinter.CTkEntry(master=self.register_frame,
                                               placeholder_text="Enter your Name/(Please Enter Your Nmae First Then Surname)",
                                               fg_color="#F0F0F0", text_color="#000", border_width=0)
        self.stu_name.pack(fill="x", pady=(12, 0), padx=27, ipady=10)

        ############### Grid For RollNo and Division
        grid = customtkinter.CTkFrame(master=self.register_frame, fg_color="transparent", height=200,
                                      width=200)
        grid.pack(fill="both", padx=27, pady=(31, 0))

        ############### RollNo label
        self.roll_no_label = customtkinter.CTkLabel(master=grid, text="Roll_No", font=("Arial Bold", 17),
                                                    text_color="#fff",
                                                    justify="left").grid(row=0,
                                                                         column=0,
                                                                         sticky="w")
        ################## RollNO Entry
        self.roll_no = customtkinter.CTkEntry(master=grid, placeholder_text="Enter Your Roll_no", fg_color="#F0F0F0",
                                              text_color="#000", border_width=0,
                                              width=250)
        self.roll_no.grid(row=1, column=0, ipady=10)

        ############### Divison Label
        self.division_label = customtkinter.CTkLabel(master=grid, text="Division", font=("Arial Bold", 17),
                                                     text_color="#fff",
                                                     justify="left").grid(row=0,
                                                                          column=1,
                                                                          sticky="w",
                                                                          padx=(
                                                                              25,
                                                                              0))
        ############### Division Entry
        self.division = customtkinter.CTkEntry(master=grid, placeholder_text="Enter Your Division", fg_color="#F0F0F0",
                                               text_color="#000", border_width=0,
                                               width=250)
        self.division.grid(row=1, column=1, ipady=10, sticky='w', padx=(25, 0))

        ############ Creating a Department Frame
        self.department = customtkinter.CTkFrame(master=self.register_frame, height=100, width=200,
                                                 fg_color="transparent")
        self.department.pack_propagate(0)
        self.department.place(x=27, y=320)

        # varibale to hold the radio button values

        self.selected_dep = tk.StringVar()

        # All department radio Button
        self.it_dep = customtkinter.CTkRadioButton(master=self.department, text="BscIt", height=5,
                                                   variable=self.selected_dep, value="BscIt",
                                                   font=("Arial Bold", 14), text_color="#fff", fg_color="#fff",
                                                   border_color="#fff",
                                                   hover_color="#F49A44"
                                                   )
        self.it_dep.grid(row=4, column=0, sticky="w", pady=(16, 0))

        self.bcom_dep = customtkinter.CTkRadioButton(master=self.department, text="BCom", variable=self.selected_dep,
                                                     value="BCom",
                                                     font=("Arial Bold", 14), text_color="#fff", fg_color="#fff",
                                                     border_color="#fff"
                                                     # hover_color="#F49A44",command=show_selection,
                                                     )
        self.bcom_dep.grid(row=5, column=0, sticky="w", pady=(16, 0))

        self.bms_dep = customtkinter.CTkRadioButton(master=self.department, text="BMS", variable=self.selected_dep,
                                                    value="BMS",
                                                    font=("Arial Bold", 14), text_color="#fff", fg_color="#fff",
                                                    border_color="#fff",
                                                    hover_color="#F49A44"
                                                    )
        self.bms_dep.grid(row=6, column=0, sticky="w", pady=(16, 0))

        # department label________________________________________________________________
        self.department = customtkinter.CTkLabel(master=self.register_frame, text="Select Your Department",
                                                 font=("Arial Bold", 17), text_color="#fff", justify="left")
        self.department.place(x=27, y=300)
        #Year________________________________________________________________________________
        self.year_label = customtkinter.CTkLabel(master=self.register_frame, text="In Which Year Are You",
                                                 font=("Arial Bold", 17), text_color="#fff")
        self.year_label.place(x=305, y=300)

        self.year_entry = customtkinter.CTkEntry(master=self.register_frame, placeholder_text="FY / SY / TY"
                                                 , fg_color="#F0F0F0", text_color="#000", border_width=0,
                                                 width=250, height=45)
        self.year_entry.place(x=305, y=350)
        #Email_____________________________________________________________________________________________
        self.email_label = customtkinter.CTkLabel(master=self.register_frame, text="Email", text_color="#fff",
                                                  font=("Arial Bold", 17))
        self.email_label.place(x=200, y=420)

        self.email_entry = customtkinter.CTkEntry(master=self.register_frame,
                                                  placeholder_text="example@gmail.com"
                                                  , fg_color="#F0F0F0", text_color="#000", border_width=0,
                                                  width=300, height=45)
        self.email_entry.place(x=200, y=450)

        # register button________________________________________________________________________
        self.accept_btn_frame=customtkinter.CTkFrame(master=self.register_frame, width=830,
                                                     height=45,
                                                      fg_color="transparent"
                                                     )
        self.accept_btn_frame.propagate(0)
        self.accept_btn_frame.pack(
            side="bottom", padx=(27, 50), pady=(27, 10), fill="both"  # Adjust padding as needed
        )
        self.Accept_Credential = customtkinter.CTkButton(master=self.accept_btn_frame, text="Accept Credential", width=830,
                                                     height=45,
                                                     font=("Arial Bold", 17), fg_color="#EE6B06", hover_color="#B0510C",command=lambda:self.switchFrame(self.Accept_Credential)
                                                     )

        self.Accept_Credential.pack()



    def switchFrame(self,button):
        # Get the button that called the function (sender)
        button_text= button.cget("text")  # Assuming you have a reference to the button that called it

        # Check which button was pressed and show the corresponding frame
        if button_text == "Register":
            self.current_right_frame.forget()
            self.left_view_for_wel.pack(side="left")
            self.register()
            self.current_right_frame = self.register_frame

        elif button_text == "Login":

            self.current_right_frame.forget()
            self.left_view_for_wel.pack(side="left")
            self.login()
            self.current_right_frame = self.login_frame

        elif button_text == "Admin":

            self.current_right_frame.forget()
            self.left_view_for_wel.pack(side="left")
            self.admin()
            self.current_right_frame = self.admin_frame

        elif button_text == "Accept Credential":
            # self.current_right_frame.forget()
            self.left_view_for_wel.pack(side="left")
            self.widget_values()
            # self.register_webcam()
            self.current_right_frame = self.register_frame

        elif button_text == "Next":
            self.current_right_frame.forget()
            self.left_view_for_wel.pack(side="left")
            self.register_webcam()
            self.current_right_frame = self.register_webcam_frame


        elif button_text == "Login":
            self.current_right_frame.forget()
            self.left_view_for_wel.pack(side="left")
            self.login()
            self.current_right_frame = self.login_frame



    def widget_values(self):
        self.Name=self.stu_name.get()
        self.Roll=self.roll_no.get()
        self.Division=self.division.get()
        self.Department=self.selected_dep.get()
        self.Year=self.year_entry.get().upper()
        self.Email=self.email_entry.get()

        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client[self.Department]  # Replace "your_database_name" with your actual database name
        collection = db[self.Year]  # Replace "your_collection_name" with your actual collection name

        existing_document = collection.find_one({"_id": self.Roll})

        if existing_document:
            CTkMessagebox(master=self.register_frame, message="Document with this Roll ID already exists",
                          title="Duplicate Roll ID", icon="cancel")


        if not all([self.Name, self.Roll, self.Division, self.Department, self.Year, self.Email]) :
            CTkMessagebox(master=self.register_frame, message="PLEASE FILL ALL THE FIELDS", title="Required"
                          , icon="cancel")


        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.Email):
            CTkMessagebox(master=self.register_frame,message="PLEASE ENTER VALID EMAIL",title="Valdiation"
                          ,icon="images/invalidemail.png")


        else:


                self.accept_btn_frame.forget()
                self.go_to_webcam= customtkinter.CTkButton(master=self.register_frame, text="Next", width=830,
                                                         height=45,
                                                         font=("Arial Bold", 17), fg_color="#EE6B06", hover_color="#B0510C",command=lambda :[self.switchFrame(self.go_to_webcam),self.send_email()]
                                                            )
                self.go_to_webcam.propagate(0)
                self.go_to_webcam.pack(
                    side="bottom", padx=(27, 50), pady=(27, 10), fill="both"  # Adjust padding as needed
                )



    def send_email(self):

        email = "17aditaya@gmail.com"
        email_paa = "zmpu vrne ebcl yolb"

        receiver_email = self.Email
        name = self.Name.title().strip()
        boldname = "<b>{}</b>".format(name)
        grret = "Thank You for joining us".title().strip()
        boldgreet = "<b>{}</b>".format(grret)
        n = "Aditya Gupta".title().strip()
        bn = "<b>{}</b>".format(n)

        subject = "Welcome to FaceRecognition Based Attendance System "
        message = (
            f"Dear {boldname},</span>\n\n"
            "Welcome to our face recognition based attendance system! 🎉 "
            "We would like to express our gratitude for choosing to join us. "
            "Allow me to introduce myself: "
            f"I am {bn}, and it's my pleasure to guide you through everything you need for success.\n"
                
            "We're thrilled to have you join our innovative approach to tracking attendance. "
            "With this system, signing in will be as easy as a smile. "
            "If you have any questions or need assistance getting started,"
            " feel free to reach out. Here's to a seamless and efficient attendance experience ahead! 😊"
            f"{boldgreet}"
        )

        em = EmailMessage()
        em["From"] = email
        em["To"] = receiver_email
        em["Subject"] = subject
        em.add_alternative(message, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email, email_paa)
            smtp.sendmail(email, receiver_email, em.as_string())

        print("Email sent successfully")

    def add_webcam(self, label):
        if "cap" not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 550)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_RGB2BGR)
        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(10, self.process_webcam)

    def register_webcam(self):
        self.register_webcam_frame = customtkinter.CTkFrame(master=self, fg_color="#204B6B", corner_radius=0,
                                                     width=750, height=750)
        self.register_webcam_frame.pack_propagate(0)
        self.register_webcam_frame.pack(side="right", padx=(1, 0))

        self.register__webcam = customtkinter.CTkFrame(master=self.register_webcam_frame, fg_color="#204B6B", corner_radius=0,
                                                  width=750, height=750)
        self.register__webcam.pack_propagate(0)
        self.register__webcam.pack(side="right", padx=(1, 0))

        # adding a webcam
        self.webcam_label = util.get_img_label(self.register__webcam)
        self.webcam_label.place(x=150, y=50)
        self.add_webcam(self.webcam_label)

        # adding a button
        self.capture_btn = customtkinter.CTkButton(master=self.register__webcam, text="Capture", width=1,
                                                   font=("Arial Bold", 17), hover_color="#B0510C",
                                                   fg_color="#EE6B06", text_color="#fff",command=lambda :[self.save_user_imag(),self.add_data_to_database()]).pack(
            fill="both", side="bottom",
            pady=(27, 50), ipady=10,

            padx=(27, 27))

    def save_user_imag(self):

            try:
                with open("encodingOfKnow.p", "rb") as file:
                    self.newUserEncoding = pickle.load(file)
            except (EOFError, FileNotFoundError):
                print("file not found")

            ret, frame = self.cap.read()
            frameS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)
            user_encoding = face_recognition.face_encodings(frameS)

            if user_encoding:

                self.is_registered = False
                for saved_encoding, database_info in self.newUserEncoding:
                    match = face_recognition.compare_faces([saved_encoding], user_encoding[0])
                    if match[0]:
                        self.is_registered = True
                        break

                if self.is_registered:
                    database_name, collection_name, document_id = database_info.split("_")
                    client = pymongo.MongoClient("mongodb://localhost:27017")
                    db = client[database_name]
                    collection = db[collection_name]
                    fields_to_retrieve = {"name": 1}
                    document = collection.find_one({"_id": document_id})
                    name=document.get("name","")
                    department, year ,roll= database_info.split("_")
                    bold_font = font.Font(weight="bold")
                    message = f"\nRoll No: {roll}\nDepartment: {department}\nYear: {year}\nName:{name}"
                    directory = "captureWebCam"

                    CTkMessagebox(title="Capturing you", message=f"You are already registered with {message}", icon=f"{directory}/{database_info}.png",
                                  icon_size=[50, 50],bg_color="red")
                else:
                    self.most_recent_capture_pil.save(f"captureWebcam/{self.Department}_{self.Year}_{self.Roll}.png")

                    CTkMessagebox(title="Capturing you", message="Capture Successfully", icon="imageCapture.png",
                                  icon_size=[50, 50])

                    self.directory_path = "captureWebCam"
                    self.image_path = f"{self.Department}_{self.Year}_{self.Roll}.png"
                    self.get_path = os.path.join(self.directory_path, self.image_path)

                    print("encoding start ")
                    self.img = cv2.imread(self.get_path)
                    self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

                    self.encode = face_recognition.face_encodings(self.img)[0]
                    print("encoding end")

                    self.UserEncodingName = f"{self.Department}_{self.Year}_{self.Roll}"
                    self.newUserEncoding.append([self.encode, self.UserEncodingName])

                    with open("encodingOfKnow.p", "wb") as file:
                        pickle.dump(self.newUserEncoding, file)

                    print("file saved")

                    print("All the encoding and Names")
                    for encoding, encodingName in self.newUserEncoding:
                        print(encoding[0], encodingName)


    def add_data_to_database(self):
        if self.is_registered == True:
            pass
            # CTkMessagebox(master=self, message="cant save your data ", icon="check")

        else:
            connection_string = "mongodb://localhost:27017"
            client = pymongo.MongoClient(connection_string)

            self.BscIt = client["BscIt"]
            self.BMS = client["BMS"]
            self.BCOM = client["BCom"]

            valid_years_per_dept = {
                "BscIt": ["FY", "SY", "TY"],
                "BCom": ["FY", "SY", "TY"],
                "BMS": ["FY", "SY", "TY"],
            }

            time_stamp = datetime.datetime.now()
            last_attendance_time = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "_id": self.Roll,
                "name": self.Name,
                "Division": self.Division,
                "email": self.Email,
                "time": f" {time_stamp.hour:01d}:{time_stamp.minute:01d}:{time_stamp.second:01d}",
                "Attendance_Count": 0,
                "last_attendance_time": last_attendance_time,

            }

            collection = None
            if self.Department == "BCom":
                if self.Year in valid_years_per_dept[self.Department]:
                    if self.Year == "FY":
                        collection = self.BCOM["FY"]
                    elif self.Year == "SY":
                        collection = self.BCOM["SY"]
                    else:
                        collection = self.BCOM["TY"]
            elif self.Department == "BscIt":
                if self.Year in valid_years_per_dept[self.Department]:
                    if self.Year == "FY":
                        collection = self.BscIt["FY"]
                    elif self.Year == "SY":
                        collection = self.BscIt["SY"]
                    else:
                        collection = self.BscIt["TY"]
            elif self.Department == "BMS":
                if self.Year in valid_years_per_dept[self.Department]:
                    if self.Year == "FY":
                        collection = self.BMS["FY"]
                    elif self.Year == "SY":
                        collection = self.BMS["SY"]
                    else:
                        collection = self.BMS["TY"]
            else:
                print("Invalid department entered!")
                return  # Exit if department is invalid

            # Insert data if collection is valid
            if collection is not None:
                collection.insert_one(data)
                # CTkMessagebox(master=self, message="Data  saved", icon="check")
            else:
                print("Invalid year for", self.Department, "department!")


            client.close()


    def login(self):
        self.login_frame = customtkinter.CTkFrame(master=self, fg_color="#204B6B", corner_radius=0,
                                             width=750, height=750)
        self.login_frame.pack_propagate(0)
        self.login_frame.pack(side="right", padx=(1, 0))

        self.login_btn = customtkinter.CTkButton(master=self.login_frame, text="Login", width=1,
                                                  font=("Arial Bold", 17), hover_color="#B0510C",
                                                  fg_color="#EE6B06", text_color="#fff",command=self.login_user
                                                  ).pack(
            fill="both", side="bottom",
            pady=(27, 50), ipady=10,
            padx=(27, 27))

        # adding a webcam
        self.webcam_label = util.get_img_label(self.login_frame)
        self.webcam_label.place(x=150, y=50)
        self.add_webcam(self.webcam_label)

    def login_user(self):

       try:
           with open("encodingOfKnow.p", "rb") as file:
               self.newUserEncoding = pickle.load(file)
       except (EOFError, FileNotFoundError):
           print("File not found")

       ret, frame = self.cap.read()
       frameS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
       frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)
       user_encoding = face_recognition.face_encodings(frameS)
       if user_encoding:
           for saved_encoding, database_info in self.newUserEncoding:
               match = face_recognition.compare_faces([saved_encoding], user_encoding[0])
               if match[0]:
                   database_name, collection_name, document_id = database_info.split("_")
                   client = pymongo.MongoClient("mongodb://localhost:27017")
                   db = client[database_name]
                   collection = db[collection_name]
                   document = collection.find_one({"_id": document_id})

                   if document:

                       today1 = datetime.datetime.today().date()
                       time_str = document.get("last_attendance_time", "").strip()
                       time1 = datetime.datetime.combine(today1, datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").time())
                       current_time = datetime.datetime.now().replace(microsecond=0)
                       time1_timestamp = time1.timestamp()
                       current_time_timestamp = current_time.timestamp()
                       time_difference = current_time - time1
                       # time_difference_seconds =  current_time_timestamp - time1_timestamp

                       if time_difference.total_seconds() > 20:  # Check if last attendance was more than 30 minutes ago
                           # Update last attendance time
                           collection.update_one({"_id": document_id}, {
                               "$set": {"last_attendance_time": current_time.strftime("%Y-%m-%d %H:%M:%S")}})

                           # Check daily login limit
                           today = datetime.datetime.today()
                           login_count = document.get("login_count", 0)
                           last_login = document.get("last_login", None)
                           if not last_login or (today - last_login).days >= 1:
                               # Reset login count and last login if 24 hours have passed
                               collection.update_one({"_id": document_id},
                                                     {"$set": {"login_count": 0, "last_login": today}})
                           elif login_count >= 8:
                              CTkMessagebox(master=self.login_frame,title="Login User",
                                                     message="Daily login limit reached. Please try again tomorrow.")
                              return

                           # Increment login count
                           collection.update_one({"_id": document_id}, {"$inc": {"login_count": 1}})
                           collection.update_one({"_id": document_id}, {"$inc": {"Attendance_Count": 1}})

                           message = "\n".join([f"{key}: {value}" for key, value in document.items()])
                           # Successful login message
                           directory="captureWebCam"
                           CTkMessagebox(master=self.login_frame,title="Login User",message= f"Login Successfully\n{message}",icon=f"{directory}/{database_info}.png",icon_size=[195, 258], height=400, width=600)
                           return
                       else:
                           remaining_secods=20-int(time_difference.total_seconds())
                           message=f"Come back after{remaining_secods}second."
                           CTkMessagebox(master=self.login_frame,title="Login User",message= message)
                           return
                   else:
                       CTkMessagebox(master=self.login_frame,title="Login User", message="User information not found in the database.")
                       return

           CTkMessagebox(master=self.login_frame,title="Login User", message="User not recognized.")
       else:
           CTkMessagebox(master=self.login_frame,title="Login User", message="No face detected.")




    def admin(self):
        self.admin_frame = customtkinter.CTkFrame(master=self, fg_color="#204B6B", corner_radius=0,
                                                  width=750, height=750)
        self.admin_frame.pack_propagate(0)
        self.admin_frame.pack(side="right", padx=(1, 0))

        self.label = customtkinter.CTkLabel(master=self.admin_frame, text="Delete User/students",
        font=("Arial Bold", 20), text_color="#fff").pack(side="top",pady=(25, 0),padx=30)

        ############ Creating a Department Frame
        self.department = customtkinter.CTkFrame(master=self.admin_frame, height=100, width=200,
                                                 fg_color="transparent")
        self.department.pack_propagate(0)
        self.department.place(x=27, y=100)

        # varibale to hold the radio button values

        self.selected_dep2 = tk.StringVar()

        # All department radio Button
        self.it_dep = customtkinter.CTkRadioButton(master=self.department, text="Bscit", height=5,
                                                   variable=self.selected_dep2, value="BscIt",
                                                   font=("Arial Bold", 14), text_color="#fff", fg_color="#fff",
                                                   border_color="#fff",
                                                   hover_color="#F49A44"
                                                   )
        self.it_dep.grid(row=4, column=0, sticky="w", pady=(16, 0))

        self.bcom_dep = customtkinter.CTkRadioButton(master=self.department, text="BCom", variable=self.selected_dep2,
                                                     value="BCom",
                                                     font=("Arial Bold", 14), text_color="#fff", fg_color="#fff",
                                                     border_color="#fff"
                                                     # hover_color="#F49A44",command=show_selection,
                                                     )
        self.bcom_dep.grid(row=5, column=0, sticky="w", pady=(16, 0))

        self.bms_dep = customtkinter.CTkRadioButton(master=self.department, text="BMS", variable=self.selected_dep2,
                                                    value="BMS",
                                                    font=("Arial Bold", 14), text_color="#fff", fg_color="#fff",
                                                    border_color="#fff",
                                                    hover_color="#F49A44"
                                                    )
        self.bms_dep.grid(row=6, column=0, sticky="w", pady=(16, 0))

        # department label________________________________________________________________
        self.department = customtkinter.CTkLabel(master=self.admin_frame, text="Select Your Department",
                                                 font=("Arial Bold", 17), text_color="#fff", justify="left")
        self.department.place(x=27, y=80)

        self.label_year = customtkinter.CTkLabel(master=self.admin_frame, text="Select Year",
                                            font=("Arial Bold", 17), text_color="#fff").pack(side="top", pady=(27, 0),
                                                                                             padx=30)

        self.entry_year=customtkinter.CTkEntry(master=self.admin_frame,placeholder_text="Enter Your Year",height=50,width=150,fg_color="white"
                                               ,text_color="black",font=("Arial",12))

        self.entry_year.pack(side="top", pady=(30, 0),padx=30)

        self.label_rollno = customtkinter.CTkLabel(master=self.admin_frame, text="Select Roll_No",
                                                 font=("Arial Bold", 17), text_color="#fff").place(x=500,y=80)


        self.entry_rollno = customtkinter.CTkEntry(master=self.admin_frame, placeholder_text="Enter Your Roll No", height=50,
                                                 width=150, fg_color="white"
                                                 , text_color="black", font=("Arial", 12))

        self.entry_rollno.place(x=500,y=138)

        self.remove_user_btn = customtkinter.CTkButton(master=self.admin_frame, text="Remove User", width=1,
                                                   font=("Arial Bold", 17), hover_color="#B0510C",
                                                   fg_color="#EE6B06", text_color="#fff",
                                                   command=lambda :[self.remove_encoding_from_list(),self.remove_entry_from_database()]).pack(
            fill="both", side="bottom",
            pady=(27, 10), ipady=10,

            padx=(27, 27))
        self.get_total_attendance = customtkinter.CTkButton(master=self.admin_frame, text="Get Your Total Attendance", width=1,
                                                       font=("Arial Bold", 17), hover_color="#B0510C",
                                                       fg_color="#EE6B06", text_color="#fff",command=self.plot_total_attendance).pack(
            fill="both", side="bottom",
            pady=(20, 5), ipady=10,

            padx=(27, 27))

    def plot_total_attendance(self):
        self.remove_department = self.selected_dep2.get()
        self.remove_year = self.entry_year.get().upper()
        self.remove_roll = self.entry_rollno.get()
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017")
            db = client[self.remove_department]
            collection = db[self.remove_year]
            document = collection.find_one({"_id": self.remove_roll})

            # Remove the entry from the database
            student_attendance=  document.get("Attendance_Count")
            student_name = document.get("name")
            print(student_attendance)
            print(student_name)
            # Create bar graph
            plt.bar(student_name, student_attendance, color='green')

            # Add labels and title
            plt.xlabel('User Name')
            plt.ylabel('Total Attendance')
            plt.title('Total Attendance by User')

            # Show the plot
            plt.show()

        except Exception as e:
            CTkMessagebox(title="Error", message="User Not Found")
    def remove_encoding_from_list(self):

            self.remove_department = self.selected_dep2.get()
            self.remove_year = self.entry_year.get().upper()
            self.remove_roll = self.entry_rollno.get()

            self.remove_user = f"{self.remove_department}_{self.remove_year}_{self.remove_roll}"
            self.image_dir = "captureWebCam"
            self.remove_image = os.path.join(self.image_dir, f"{self.remove_user}.png")

            print(self.remove_image)

            try:
                if os.path.exists(self.remove_image):
                    os.remove(self.remove_image)
                    print(f"Image {self.remove_image} removed successfully.")
                    CTkMessagebox(master=self.admin_frame,message=f"Image {self.remove_image} removed successfully.",title="Removing User Image")

                    updated_encoding_list = []
                    with open("encodingOfKnow.p", "rb") as file:
                        self.newUserEncoding = pickle.load(file)

                    # Remove the encoding corresponding to the deleted image
                    for encoding, user in self.newUserEncoding:
                        if user != self.remove_user:
                            updated_encoding_list.append([encoding, user])
                            CTkMessagebox(master=self.admin_frame,message="Deleted Succssfully",title="Removing User")

                    # Save the updated encoding list
                    with open("encodingOfKnow.p", "wb") as file:
                        pickle.dump(updated_encoding_list, file)
                        print("file updated")
                else:
                    print(f"Image {self.remove_image} does not exist.")
            except Exception as e:
                CTkMessagebox(title="Error", message=str(e))

    def remove_entry_from_database(self):
        self.remove_department = self.selected_dep2.get()
        self.remove_year = self.entry_year.get().upper()
        self.remove_roll = self.entry_rollno.get()
        try:
            client = pymongo.MongoClient("mongodb://localhost:27017")
            db= client[self.remove_department]
            collection = db[self.remove_year]

            # Remove the entry from the database
            collection.delete_one({"_id": self.remove_roll})

            client.close()
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))


app = App()

app.mainloop()
