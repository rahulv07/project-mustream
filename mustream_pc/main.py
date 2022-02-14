from audio import Audio
from mySocket import MySocket

if __name__ == "__main__":
    
    audio = Audio()
    audio.startPyAudio(fs=44000,channels=1,chunkSize=1024)

    mySocket = MySocket()
    
    print(f"\nServer IP address: {mySocket.getIP()}")
    
    mySocket.startServer(port=5902)
    (client,addr) = mySocket.getClient()
    print(f"Connected {addr}")
    
    audio.setSpeakerAsInput()
    
    print("Recording Started...")
    i = 0
    
    while True:
        try:
            audioPacket = audio.record(seconds=1)
            client.sendall(audioPacket)
            print(f"Sent {len(audioPacket)} bytes")
            i = i+1
            response = client.recv(1024)
        except KeyboardInterrupt:
            audio.closePyAudio()
            client.close()
            mySocket.closeServer()
            break
        
    print("Recording Stopped!")
    print(f"Packets sent: {i}")
    
    
    audio.setMicAsInput()