import numpy as np
from audio import Audio
from scipy.io import wavfile

host = '192.168.160.110'
port = 5902

audio = Audio(host,port)
audio.speakerTransmit()


#At 44k sampling rate, packets of size 86060 bytes are transmitted every second
