#!/usr/bin/env python
"""
Program Name: network scanner
Description: Scans the network and provides the IP and MAC address of network users.

Requirements:
    Runs on Python 2 or 3

Author: CoderMANE
Date: 2024-06-09
"""

import scapy.all as scapy
import socket

def get_local_ip():
    """Get the local IP address of the current machine."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None

# Scans and returns clients into a dictionary
def scan(ip):
    arp_request = scapy.ARP(pdst=ip + "/24")  # Scan the entire subnet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

# Handles output
def print_result(results_list):
    print("IP\t\t\tMAC Address\n----------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

# Get local IP and scan the network
local_ip = get_local_ip()
if local_ip:
    scan_result = scan(local_ip)
    print_result(scan_result)
else:
    print("Could not determine local IP.")
