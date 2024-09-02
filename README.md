creating a pensuite to run basic test for attack creation

arp spoofer changes network router to send request first through your computer then target

spoof_detector can check your network to see if your in an MITM attack

dns_spoofer changes requested website to your desired address

mac changer changes your mac address to desired mac

network scanner lists the current ip and mac of all devices on your current network

packet sniffer collects potential credentials of target who visit http websites on your current network

useful commmands
  -ssl_striping
  bettercap -iface eth0 -caplet hstshijack/hstshijack
  
  -fowarding 
  echo 1 > /proc/sys/net/ipv4/ip_forward

  -table creation
  iptables -I FORWARD -j NFQUEUE --queue-num 0
