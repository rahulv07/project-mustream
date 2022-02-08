from audio import Audio
import pyaudio
import wave
import subprocess

# # host = '192.168.13.115'
# # port = 5902

# # audio = Audio(host,port)

def recordSpeakerOutput():
    recordSpeakerCommand = "pacmd set-default-source alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"
    recordMicCommand = "pacmd set-default-source alsa_input.pci-0000_00_1b.0.analog-stereo"
    try:
        subprocess.call(recordSpeakerCommand,shell=True)
    except Exception as e:
        print("Error: "+str(e))
        
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")
    
    try:
        subprocess.call(recordMicCommand,shell=True)
    except Exception as e:
        print("Error: "+str(e))

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    

recordSpeakerOutput()
