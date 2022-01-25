import socket
import threading, wave, pyaudio,pickle,struct

host_ip = '192.168.253.63'#  socket.gethostbyname(host_name)
port = 4444

def audio_stream():

    CHUNK = 1024
    wf = wave.open("temp.wav", 'rb')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

             

    #client_socket,addr = server_socket.accept()
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.connect((host_ip,port))

    data = None 

    (nchannels,sampwidth,fs,nframes,_,_) = wf.getparams()

    readData = 0
    npackets = 1
    while True:
        data = wf.readframes(CHUNK)
        readData = readData + (CHUNK*sampwidth)
        a = pickle.dumps(data)
        message = struct.pack("Q",len(a))+a
        server_socket.sendall(message)
        if(readData>=sampwidth*nframes): break
        print(f"Packets sent: {npackets}")
        npackets = npackets+1
                
t1 = threading.Thread(target=audio_stream, args=())
t1.start()

