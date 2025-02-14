import os
import subprocess

def get_scripts():
    scripts = []
    for root, dirs, files in os.walk("../modules"):
        for file in files:
            if file.endswith(".py"):
                scripts.append(file)
    return scripts

class ScriptLoader:
    def __init__(self):
        self.scripts = {}
        self.payload = None

    # run python script
    def run_script(self, arg=None):
        try:
            print(f"Running script: {self.payload}")
            if arg is None:
                result = subprocess.run([f"python3 ../modules/{self.payload}"],
                                        shell=True,
                                        capture_output=True,
                                        text=True)
            else:
                result = subprocess.run([f"python3 ../modules/{self.payload} {arg}"],
                                        shell=True,
                                        capture_output=True,
                                        text=True)
            print(result.stdout)
        except Exception as e:
            print(f"Error: {e}")

    # set python script
    def set_script(self):
        user_input = int(input("Enter script: "))
        print(f"Script selected: {self.scripts[user_input]}")
        self.payload = self.scripts[user_input]

    # load python scripts
    def load_scripts(self):
        counter = 1
        for script in get_scripts():
            self.scripts[counter] = script
            counter += 1
        return self.scripts
    
    # view python scripts
    def view_scripts(self):
        for key, value in self.scripts.items():
            print(f"{key}: {value}")
