#! /usr/bin/env python3

class SocketFramed:

    def __init__(self, connectedSocket):     # to make a new framed socket
        self.cs = connetedSocket
        self.buff = ""

    def sendMessage(self, message):     # sends an out of band framed message
        msglen = str(len(message))
        msg = msglen.encode()+b":"+message
        
        while len(msg):
            bytes = self.cs.send(msg)
            msg = msg[bytes:]

    def receiveMessage(self):      # receives a framed message and returns the entire message
        if self.buff == "":
            self.buff += self.cs.recv(100).decode()

        lenMsg = ""

        while True:      # gets the message length
            if len(self.buff) == 0:
                self.buff = self.cs.recv(100).decode()

            if self.buff[0] == ":":
                self.buff = self.buff[1:]
                break

            lenMsg += self.buff[0]
            self.buff = self.buff[1:]

        if (lenMsg == ""):
            return ""

        intlenMsg = int(lenMsg)
        msg = ""

        while ((len(msg) < intlenMsg)):     # while length of built in msg < length in framing
            if (len(self.buff) == 0):
                self.buff = self.cs.recv(100).decode()

            msg += self.buff[0]
            self.buff = selfself.buff[1:]

            return msg
    
    
