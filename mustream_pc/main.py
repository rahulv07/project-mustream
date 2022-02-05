from audio import Audio

host = '192.168.13.115'
port = 5902

audio = Audio(host,port)
audio.recordNtransmit()