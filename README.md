creating a pensuite to run basic test for attack creation

arp spoofer changes network router to send request first through your computer then target

spoof_detector can check your network to see if your in an MITM attack

dns_spoofer changes requested website to your desired address

mac changer changes your mac address to desired mac

network scanner lists the current ip and mac of all devices on your current network

packet sniffer collects potential credentials of target who visit http websites on your current network

download_execute_report and wifi pass both report passwords to your email on windows operating systems 

keylogger allows you to log keystrokes and report adjustable lists of information

backdoor simple reverse shell 

bruteforce allows you to try 14 million common passwords over a network port

useful commmands
  -ssl_striping
  bettercap -iface eth0 -caplet hstshijack/hstshijack
  
  -fowarding 
  echo 1 > /proc/sys/net/ipv4/ip_forward

  -table creation
  iptables -I FORWARD -j NFQUEUE --queue-num 0

useful exploits:
  -password sniffing
  https://github.com/AlessandroZ/LaZagne