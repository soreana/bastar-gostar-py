#!/usr/bin/python

import socket
import threading
import sys
from time import sleep

# if false disable debug lines
debug = False

if len(sys.argv) >= 2 and sys.argv[1] == "debug":
    print "entering debug mode."
    debug = True

# set up server
s = socket.socket()
host = '0.0.0.0'
port = 8000
s.bind((host, port))

s.listen(5)  # up to 5 concurrent connections


def secretary():
    c, addr = s.accept()  # Establish connection with client.
    if debug:
        print 'Got connection from', addr
    c.send('Bah Bah')
    c.close()
    return


threads = []
while True:
    t = threading.Thread(target=secretary)
    threads.append(t)
    sleep(2)
    t.start()
e