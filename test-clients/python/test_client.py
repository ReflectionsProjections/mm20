import socket

HOST = 'localhost'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Initial connection data') #TODO: send actual stuff
data = s.recv(1024)
while len(data) > 0: #TODO: Need check for game over
    print 'Received', repr(data)
    s.sendall('{}') #TODO: send actual stuff
    data = s.recv(1024)
s.close()