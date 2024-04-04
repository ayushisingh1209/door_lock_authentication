import os.path
import datetime
import pickle
import pyttsx3
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import serial
import util
import sys

sys.path.append(r'C:\Users\VIVEK KUMAR SINGH\Desktop\facedetection\Silent-Face-Anti-Spoofing-master')
from testing import test
import getpass
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 140)
engine.setProperty("volume", 1000)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


class App:

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if not ret or frame is None:
            # Handle the case where the frame is empty or None
            # You can choose to display an error message or take other appropriate actions
            print("Error: Empty or None frame")
            return
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):

        label = test(
            image=self.most_recent_capture_arr,
            model_dir=r'C:\Users\VIVEK KUMAR SINGH\Desktop\facedetection\Silent-Face-Anti-Spoofing-master\resources\anti_spoof_models',
            device_id=0
        )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
                speak('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
                speak("Welcome back ")
                # ard = serial.Serial('com9' ,9600)
                # time.sleep(2)
                # var = 'a'
                # c=var.encode()
                # speak("Face recognition complete..it is matching with database...welcome..sir..Door is openning for 5 seconds")
                # ard.write(c)
                # time.sleep(4)
                with open(self.log_path, 'a') as f:
                    f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                    f.close()

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')
            speak("Hey, you are a spoofer!', 'You are fake !")

    def logout(self):

        label = test(
            image=self.most_recent_capture_arr,
            model_dir=r'C:\Users\VIVEK KUMAR SINGH\Desktop\facedetection\Silent-Face-Anti-Spoofing-master\resources\anti_spoof_models',
            device_id=0
        )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
                speak('Ups...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Hasta la vista !', 'Goodbye, {}.'.format(name))
                speak('Goodbye')
                with open(self.log_path, 'a') as f:
                    f.write('{},{},out\n'.format(name, datetime.datetime.now()))
                    f.close()

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')
            speak('Hey, you are a spoofer!', 'You are fake !')

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("400x200+500+200")

        self.password_entry = util.get_password_entry(self.register_new_user_window)
        self.password_entry.place(x=150, y=50)

        self.password_label = util.get_text_label(self.register_new_user_window, 'Enter Password:')
        self.password_label.place(x=150, y=150)

        self.authenticate_button = util.get_button(self.register_new_user_window, 'Authenticate', 'green',
                                                   self.authenticate_password)
        self.authenticate_button.place(x=150, y=100)

    def authenticate_password(self):
        entered_password = self.password_entry.get()

        # Replace 'sherubhai' with your actual password
        if entered_password == 'sherubhai':
            self.register_new_user_window.geometry("1200x520+370+120")

            self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept',
                                                                           'green', self.accept_register_new_user)
            self.accept_button_register_new_user_window.place(x=750, y=300)

            self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window,
                                                                              'Try again', 'red',
                                                                              self.try_again_register_new_user)
            self.try_again_button_register_new_user_window.place(x=750, y=400)

            self.capture_label = util.get_img_label(self.register_new_user_window)
            self.capture_label.place(x=10, y=0, width=700, height=500)

            self.add_img_to_label(self.capture_label)

            self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
            self.entry_text_register_new_user.place(x=750, y=150)

            self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                     'Please, \ninput username:')
            self.text_label_register_new_user.place(x=750, y=70)
        else:
            util.msg_box('Invalid Password', 'Please enter the correct password.')

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)

        util.msg_box('Success!', 'User was registered successfully!')
        speak('Success! User was registered successfully!')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
