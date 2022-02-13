import pyaudio
import numpy as np
import struct
import sys
import subprocess
import platform

class Audio:

    def startPyAudio(self,fs,channels,chunkSize):
        self.rate = fs
        self.chunkSize = chunkSize
        self.channels = channels
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=channels, rate=fs, input=True, frames_per_buffer=chunkSize)

    def closePyAudio(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
    def encodeData(self,rate, data):
        output = b''
        wavBytes = b'RIFF'
        fs = rate

        try:
            dkind = data.dtype.kind
            if not (dkind == 'i' or dkind == 'f' or (dkind == 'u' and
                                                    data.dtype.itemsize == 1)):
                raise ValueError("Unsupported data type '%s'" % data.dtype)

            header_data = b'WAVE'

            header_data += b'fmt '
            if dkind == 'f':
                format_tag = 0x0003
            else:
                format_tag = 0x0001
            if data.ndim == 1:
                channels = 1
            else:
                channels = data.shape[1]
            bit_depth = data.dtype.itemsize * 8
            bytes_per_second = fs*(bit_depth // 8)*channels
            block_align = channels * (bit_depth // 8)

            fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, fs,
                                        bytes_per_second, block_align, bit_depth)
            if not (dkind == 'i' or dkind == 'u'):
                fmt_chunk_data += b'\x00\x00'

            header_data += struct.pack('<I', len(fmt_chunk_data))
            header_data += fmt_chunk_data

            if not (dkind == 'i' or dkind == 'u'):
                header_data += b'fact'
                header_data += struct.pack('<II', 4, data.shape[0])

            if ((len(header_data)-4-4) + (4+4+data.nbytes)) > 0xFFFFFFFF:
                raise ValueError("Data exceeds wave file size limit")

            output = output + header_data
            output = output + b'data'
            output += struct.pack('<I', data.nbytes)
            if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and
                                            sys.byteorder == 'big'):
                data = data.byteswap()
            output += data.ravel().view('b').data
            size = len(output)
            wavBytes += struct.pack('<I', size)
            wavBytes += output

        finally:
            return wavBytes
        
    def record(self,seconds):
        frames = []
        
        for _ in range(0,int(self.rate/ self.chunkSize * seconds)):
            data = self.stream.read(self.chunkSize)
            frames.append(np.frombuffer(data,dtype=np.int16))
            
        audioData = np.hstack(frames)
        encodedData = self.encodeData(self.rate,audioData)
        return encodedData
        
    def setSpeakerAsInput(self):
        if platform.system()=="Linux":
            self.linuxSpeakerAsInput()
            
    def setMicAsInput(self):
        if platform.system()=="Linux":
            self.linuxMicAsInput()
                
    def linuxSpeakerAsInput(self):
        setSpeakerLoopbackCommand = "pacmd load-module module-loopback latency_msec=5"
        recordSpeakerCommand = "pacmd set-default-source alsa_output.pci-0000_00_1b.0.analog-stereo.monitor"
        try:
            subprocess.call(setSpeakerLoopbackCommand,shell=True)
            subprocess.call(recordSpeakerCommand,shell=True)
        except Exception as e:
            print("Error: "+str(e))

    def linuxMicAsInput(self):
        recordMicCommand = "pacmd set-default-source alsa_input.pci-0000_00_1b.0.analog-stereo"
        try:
            subprocess.call(recordMicCommand,shell=True)
        except Exception as e:
            print("Error: "+str(e))