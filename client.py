#!/usr/bin/python

import socket
import time
import sys

# if false disable debug lines
debug = False

if len(sys.argv) >= 2 and sys.argv[1] == "debug":
    print "entering debug mode."
    debug = True

# method to get current time in millisecond
current_milli_time = lambda: int(round(time.time() * 1000))

while True:
    host = raw_input("Please enter host ip or exit to exit.\n")
    print "you entered", host

    if host == "exit":
        exit(0)

    # connect to server
    s = socket.socket()
    port = 8000

    # get current time
    t1 = current_milli_time()
    if debug:
        print "t1 is", t1

    # connect and send message to server
    s.settimeout(10)
    try:
        s.connect((host, port))
        s.settimeout(None)
        s.send("All human beings are in truth akin")
        s.recv(1024)
    except socket.timeout:
        print "timeout exception.\ncan't find route to host."

    # get current time
    t2 = current_milli_time()
    if debug:
        print "t2 is", t2

    # show delay time
    print "delay is: ", t2 - t1
    s.close()

    # to test multi thread
    if debug:
        time.sleep(1)
