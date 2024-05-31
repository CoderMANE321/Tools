#!/usr/bin/env python
import argparse

import scapy.all as scapy

def get_arguments():
    # parse user inputs
    parser = argparse.ArgumentParser()
    # describes options
    parser.add_argument("-i", "--ip", dest="ip", help="Ip to scan")

    options = parser.parse_args()
    if not options.ip:
        parser.error("[-] Please specify an ip address, use --help for more info.")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n----------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


# call and use function
options = get_arguments()
scan_result = scan(options.ip)
print_result(scan_result)
