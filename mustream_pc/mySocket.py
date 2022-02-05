import socket

class MySocket:
    def __init__(self) :
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    def openSocket(self,HOST,PORT):
        """
        Open a new socket and connect to server
        Args:
            HOST (str): IPV4 address of the server
            PORT (int): PORT number of the server
        """
        self.s.connect((HOST,PORT))
        
    def sendPackets(self,packet):
        """
        Send bytes to the server through sockets
        Args:
            packet (bytes): Bytes data
        """
        self.s.sendall(packet)
        
    def closeSocket(self):
        """
        Closes the socket connection with the server
        """
        self.s.close()