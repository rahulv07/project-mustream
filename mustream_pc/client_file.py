import socket
import wave

wf = wave.open("temp.wav")

(nChannels,sampWidth,fs,nFrames,_,_) = wf.getparams()

buffer = sampWidth * fs

HOST = '192.168.87.161' 
PORT = 5902

f = open("temp.wav","rb")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    i = 0
    while True:
        packet = f.read(buffer)
        if not packet:
            break
        s.sendall(packet)
        i = i+1
        print(f"Sending packet: {i}")

print("Transfer done")
