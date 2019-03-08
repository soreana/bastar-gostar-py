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

    while True:
        print c.recv(1024)
         
    # c.send('Bah Bah')
    #c.close()
    return


# threads = []

def parse_of_header( s ):
    if len(s) < 8:
        return 8

    length = (ord(s[3]) + ord(s[2])*2**8)

    if debug:
        print ( "version: %s" % ord(s[0]) )
        print ( "type: %s" % ord(s[1]) )
        print ( "length: %s" % length )
        print ( "xid: %s" % (ord(s[7]) + ord(s[6])*2**8 + ord(s[5])*2**16 + ord(s[4])*2**24 ))
    return length
    
def read_of_header(c):
    cur = c.recv(8)
    return parse_of_header(cur) - 8, cur

def feature_req():
    return "%s%s%s%s%s%s%s%s"%(chr(1),chr(5),chr(0),chr(8),chr(0),chr(0),chr(1),chr(240))


def connect_to_floodlight():
    s = socket.socket()
    port = 6653
    host = '127.0.0.1'
    s.connect((host, port))
    return s

while True:
    #t = threading.Thread(target=secretary)
    #threads.append(t)
    #t.start()

    c, addr = s.accept()  # Establish connection with client.
    if debug:
        print 'Got connection from', addr
    #sleep(5)
    payload_size , cur = read_of_header(c)
    print ( "start floodlight part.")
    f = connect_to_floodlight()
    f.send(cur)
    payload_size , cur = read_of_header(f)
    c.send(cur)
    print ( "done floodlight part.")

    payload_size , cur = read_of_header(f)

    c.send(feature_req())
    payload_size , cur = read_of_header(c)
    c.recv(payload_size)
    for i in range(0,4):
        payload_size , cur = read_of_header(c)
        c.recv(payload_size)
        

