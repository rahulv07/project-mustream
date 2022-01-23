import socket
import threading

hosts = ['192.168.xx.15']  # The server's hostname or IP address
port = 4444       # The port used by the server

def threadFunction(host,port,data):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((host,port))
        s.sendall(data)

for host in hosts:
    data = b'Hello Server!'
    th = threading.Thread(target=threadFunction,args=[host,port,data])
    th.start()


