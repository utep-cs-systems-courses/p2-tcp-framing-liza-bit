#! /usr/bin/env python3
#
# Server side of a tcp file transfer program

import socket, sys, re, os
sys.path.append("../lib")     # for params
from lib import params
import Worker
import framed_socket
import my_io

switchesVarDefaults = (
    (('-1','--listenPort'), 'listenPort', 50001),
    (('-?','--usage'), "usage", False),     # boolean (set if present)
    )

progname = "tcp_server"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''     # symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)     # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept()     # wait until incoming connection request (and accept it)
    Worker.Worker(conn, addr).start
