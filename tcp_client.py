#! /usr/bin/env python3

import socket, sys, re, time, os
sys.path.append("../lib")     # for params
from lib import params
import framed_socket
import my_io

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-i', '--inputf'), 'inputf', "text.txt"),
    (('-o', '--outputf'), 'outputf', "text.txt"),
    (('-?', '--usage'), "usage", False),     # booelan (set if present)
    )

progname = "tcp_client"
#paramMap = params.parseParams(switchesVarDefaults)

# server, usage, inputf, outputf = paramMap["server"], paramMap["usage"], paramMap["inputf"], paramMap["outputf"]

#if usage:
    #params.usage()


try:    # tries to get the necessary parameters
    tcp_client = sys.argv[1]
    serverHost, serverFile = re.split(":", sys.argv[2])
    serverport = 50001

except:
    my_io.myPrint("Bad param format: '%s'. Should be $ ./tcp_server Send {clientFile} {host:serverFile} \n" % sys.argv)
    sys.exit(1)

s = None

for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        my_io.myPrint("Creating sock: af=%d, type=%d, proto=%d\n" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)

    except socket.error as msg:
        my_io.myPrint("Error: %s\n" % msg)
        s = None
        continue

    try:
        my_io.myPrint("Attempting to connect to %s\n" % repr(sa))
        s.connect(sa)

    except socket.error as msg:
        my_io.myPrint("Error: %s\n" % msg)
        s.close()
        s = None
        continue

    break

if s is None:
    my_io.myPrint('Could not open socket\n')
    sys.exit(1)

delay = float(paramMap['delay'])    # delay before reading, default = 0s
if delay != 0:
    print(f"Sleeping for {delay}s")
    time.sleep(delay)
    print("Done sleeping")

fs = framed_socket.socketFramed(s)     # a new framed socket obj

fs.sendMessage(sys.argv[0].encode())
fs.sendMessage(serverFile.encode())     # sent the file to be saved on server side

response = fs.receiveMessage()      # gets the response from the sever ("OK" or "NO")

if response == "OK":
    message = my_io.myReadFile(clientFile)    # reads the contents of the client side file
    fs.sendMessage(message.encode())
    result = fs.receiveMessage()      # receives the result of the transfer
    my_io.myPrint(result + "\n")      # prints result (SUCCESS or FAILURE WRITING FILE)

elif response == "NO":
    my_io.myPrint("File name already exists \n")    # response was a NO

else:
    my_io.myPrint("File is currently being written to \n")

s.close()
