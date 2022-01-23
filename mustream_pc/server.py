import socket

print('Running...')
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 4444))
print('Socket has been bound')
s.listen()
print("Waiting for connection...")
conn, addr = s.accept()
print('Connection has been accepted')
