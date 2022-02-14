import socket

class MySocket:
    
    def startServer(self,port):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(('',port))
        print("Server Started...")
        self.s.listen()
    
    def getClient(self):
        client,addr = self.s.accept()
        return (client,addr)
    
    def getIP(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            return ip
        
    def closeServer(self):
        self.s.close()
