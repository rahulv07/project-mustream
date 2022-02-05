import pyaudio
import numpy as np
import scipy.io.wavfile as wav
import wave
import struct
import sys

def recordAudio():
    RATE=16000
    RECORD_SECONDS = 7
    CHUNKSIZE = 1024

    # initialize portaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)

    frames = [] # A python-list of chunks(numpy.ndarray)
    print("Recording...")
    for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS)):
        data = stream.read(CHUNKSIZE)
        frames.append(np.frombuffer(data, dtype=np.int16))

    #Convert the list of numpy-arrays into a 1D array (column-wise)
    numpydata = np.hstack(frames)

    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    #wav.write('out.wav',RATE,numpydata)
    generateWAVdata(RATE,numpydata)
    
def readAudio(name):
    audioData = np.fromfile(name,dtype=np.uint8)
    print(audioData[0:11])
    

def generateWAVdata(rate, data):
    """
    =====================  ===========  ===========  =============
         WAV format            Min          Max       NumPy dtype
    =====================  ===========  ===========  =============
    32-bit floating-point  -1.0         +1.0         float32
    32-bit PCM             -2147483648  +2147483647  int32
    16-bit PCM             -32768       +32767       int16
    8-bit PCM              0            255          uint8
    =====================  ===========  ===========  =============

    Note that 8-bit PCM is unsigned.
    """
    output = b''
    wavBytes = b'RIFF'
    fs = rate

    try:
        dkind = data.dtype.kind
        if not (dkind == 'i' or dkind == 'f' or (dkind == 'u' and
                                                 data.dtype.itemsize == 1)):
            raise ValueError("Unsupported data type '%s'" % data.dtype)

        header_data = b''

        # header_data += b'RIFF'
        # header_data += b'\x00\x00\x00\x00'
        header_data += b'WAVE'

        # fmt chunk
        header_data += b'fmt '
        if dkind == 'f':
            format_tag = 0x0003
        else:
            format_tag = 0x0001   #0x0001
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
            # add cbSize field for non-PCM files
            fmt_chunk_data += b'\x00\x00'

        header_data += struct.pack('<I', len(fmt_chunk_data))
        header_data += fmt_chunk_data

        # fact chunk (non-PCM files)
        if not (dkind == 'i' or dkind == 'u'):
            header_data += b'fact'
            header_data += struct.pack('<II', 4, data.shape[0])

        # check data size (needs to be immediately before the data chunk)
        if ((len(header_data)-4-4) + (4+4+data.nbytes)) > 0xFFFFFFFF:
            raise ValueError("Data exceeds wave file size limit")

        output = output + header_data

        # data chunk
        output = output + b'data'
        output += struct.pack('<I', data.nbytes)
        if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and
                                           sys.byteorder == 'big'):
            data = data.byteswap()
        output += data.ravel().view('b').data

        # Determine file size and place it in correct
        #  position at start of the file.
        size = len(output) + 8
        wavBytes += struct.pack('<I', size-8)
        wavBytes += output

    finally:
        # if not hasattr(filename, 'write'):
        #     fid.close()
        # else:
        #     fid.seek(0)
        wavData = np.frombuffer(wavBytes,dtype=np.uint8)
        print(len(wavData))
        print(wavData[0:11])

recordAudio()