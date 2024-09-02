#!/usr/bin/env python
"""
Program Name: spoof_detector

Description: scans network for attackers running a man in the middle attack

Options:
    none , use as is


Examples:
    python packet_sniffer.py

Requirements:
    Runs on Python 2 or 3

Author: CoderMANE

Date: 2024-09-02
"""
import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            
            if real_mac != response_mac:
                print("[+] Your under attack!")
            print(packet.show)
        except IndexError:
            pass


sniff("eth0")
