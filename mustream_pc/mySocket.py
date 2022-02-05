import socket

class MySocket:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def openSocket(self,HOST,PORT):
        self.s.connect((HOST,PORT))
        
    def sendPackets(self,packet):
        self.s.sendall(packet)
        
    def closeSocket(self):
        self.s.close()