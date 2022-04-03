from audio import Audio
import asyncio
import socket

async def handle_client(reader,writer):
    audio = Audio()
    audio.startPyAudio(fs=44000,channels=1,chunkSize=1024)

    audio.setSpeakerAsInput()
    
    print("Recording Started...")
    i = 0
    
    while True:
        try:
            audioPacket = audio.record(seconds=1)
            writer.write(audioPacket)
            await writer.drain()
            print(f"Sent {len(audioPacket)} bytes")
            i = i+1
            response = await reader.read(1024)
        except KeyboardInterrupt:
            audio.closePyAudio()
            writer.close()
            break
        
    print("Recording Stopped!")
    print(f"Packets sent: {i}")    
    
    audio.setMicAsInput()


async def main():
    server = await asyncio.start_server(handle_client, '', 5902)

    async with server:
        await server.serve_forever()

def getIP():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    
if __name__ == "__main__":  
    print(f"\nServer IP address: {getIP()}")
    asyncio.run(main())