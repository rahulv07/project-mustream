import wave
import numpy as np

bytesStream = np.fromfile("temp.wav",dtype=np.uint8)

print(bytesStream[0:11])