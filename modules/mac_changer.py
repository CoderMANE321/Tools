#!/usr/bin/env python
"""
Program Name: MAC Changer

Description: Changes the MAC address of the machine's network interface.

Requirements:
    Runs on Python 2 or 3

Author: CoderMANE
Date: 2024-06-09
"""

import subprocess
import re

# Automatically detects the primary network interface
def get_interface():
    try:
        ifconfig_result = subprocess.check_output(["ip", "link"], text=True)
        interfaces = re.findall(r"^\d+: (\w+):", ifconfig_result, re.MULTILINE)
        for iface in interfaces:
            if iface != "lo":  # Ignore the loopback interface
                return iface
    except Exception as e:
        print(f"Error detecting interface: {e}")
    return None

# Changes MAC address
def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ip", "link", "set", interface, "down"])
    subprocess.call(["sudo", "ip", "link", "set", interface, "address", new_mac])
    subprocess.call(["sudo", "ip", "link", "set", interface, "up"])

# Gets current MAC address
def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ip", "link", "show", interface], text=True)
        mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
    except Exception as e:
        print(f"Error getting MAC address: {e}")
    return None

# Main execution
interface = get_interface()
if not interface:
    print("[-] No valid network interface found.")
else:
    print(f"Detected interface: {interface}")
    current_mac = get_current_mac(interface)
    print(f"Current MAC: {current_mac}")

    new_mac = "00:11:22:33:44:55"  # Change this to your desired MAC address
    change_mac(interface, new_mac)

    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print(f"[+] MAC address successfully changed to {current_mac}")
    else:
        print("[-] MAC address did not change.")
