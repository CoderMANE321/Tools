#!/usr/bin/env python
"""
Program Name: mac changer

Description: Changes the mac address of given machine ip

Options:
    -i or --i = ip address
    -m or --mac = mac address
    --help = argument options


Examples:
    python mac_changer.py -i or --i with -m or --mac
    python mac_changer.py --help

Requirements:
    Runs on Python 2 or 3

Author: CoderMANE

Date: 2024-06-09
"""
import subprocess
import optparse
import re

# collects arguments
def get_arguments():
    # parse user inputs
    parser = optparse.OptionParser()
    # describes options
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new mac, use --help for more info.")
    return options

# changes mac address
def change_mac(interface, new_mac):
    print("[+ Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

# collects the current address for check later in program
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


# call and use functions
options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
# checks if program was sucessful
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address didn't change")
