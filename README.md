!best to work from Linux in my opnion due to more control and options over operating system

!check your added exploits or custom malware at Nodistribute before running to bypass program checks


!Files

arp spoofer changes network router to send request first through your computer then target


spoof_detector can check your network to see if your in an MITM attack


dns_spoofer changes requested website to your desired address


mac changer changes your mac address to desired mac


network scanner lists the current ip and mac of all devices on your current network


packet sniffer collects potential credentials of target who visit http websites on your current network


download_execute_report and wifi pass both report passwords to your email on windows operating systems 


keylogger allows you to log keystrokes and report all keystrokes to your email


backdoor folder holds simple reverse shell with listener  


crawler checks subdomains and directories with given url


spider recursively checks root directory for all links hosted by server


bruteforce allows you to try 14 million common passwords over a network port(SSH focused)


vulnerability_scanner template scanner that comes built in with XSS


web_bruteforce allows you to test multiple passwords agaisnt a know username

!Tips

Trojans
!put exe in a archive to protect changes
!use pyinstaller to diguise file with flags --add-data "path/to/fakefile", -- and --icon "path/to/icon" 
!use character right to left overide and rename exectuable as "filename'fdp.exe'" and paste character over single quotes


web_bruteforce 
! setup proxies to switch between ip's
! use sleep command to prevent to much noise
! find username or email by using recover my password and try until it says account is found

vulnerability scanner
!more vulnerabilties will be added or you can add your own to test, similiar to YARN and adding rules

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

file compression:
  https://github.com/upx