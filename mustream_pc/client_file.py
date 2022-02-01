import socket
import numpy as np
import time

HOST = '192.168.24.40'  # The server's hostname or IP address. Localhost : 127.0.0.1
PORT = 5902        # The port used by the server

wf = open("temp.wav","rb")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    buffer = 1024
    i = 0
    while True:
        packet = wf.read(buffer)
        if not packet:
            break
        s.sendall(packet)
        i = i+1
        print(f"Sending packet: {i}")
        time.sleep(1)
        
print("Transfer done")

bytesStream = np.fromfile("temp.wav",dtype=np.uint8)
print(len(bytesStream))