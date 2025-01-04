#!usr/bin/env/python

import requests

target_url = "google.com"
"""
    sends a request to the target url and crawls the website for subdomains and directories
"""
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

# subdomains
with open("/root/Downloads/subdomains-10000.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        if response:
            print("[+] Discovered subdomain: " + test_url)

# directories
with open("/root/Downloads/directory-list-2.3-medium.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered subdomain: " + test_url)