#!/usr/bin/env python
"""
Program Name: spoof_detector

Description: Scans network for attackers running a man-in-the-middle attack.

Options:
    None, use as is.

Examples:
    python packet_sniffer.py

Requirements:
    Runs on Python 2 or 3

Author: CoderMANE

Date: 2024-09-02
"""
import scapy.all as scapy
import threading
import time

TIMEOUT = 30  # Stop sniffing after 30 seconds


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    return answered_list[0][1].hwsrc if answered_list else None


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac and real_mac != response_mac:
                print("[+] You're under attack!")
                print(packet.show)
            else:
                print("[+] You're all good")
        except IndexError:
            pass


def sniff_packets(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, timeout=TIMEOUT)


# Run sniffing in a separate thread
sniff_thread = threading.Thread(target=sniff_packets, args=("eth0",))
sniff_thread.start()

# Allow script to wait for the sniffing to complete
sniff_thread.join()

print("\n[+] Sniffing stopped after 30 seconds.")
