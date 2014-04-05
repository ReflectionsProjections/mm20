import socket

HOST = 'localhost'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('{"team":"test", "members":[{"name":"test1", "class":"test"},{"name":"test2", "class":"test"},{"name":"test3", "class":"test"}]}')
data = s.recv(1024)
while len(data) > 0: #TODO: Need check for game over
    print 'Received', repr(data)
    s.sendall('{}') #TODO: send actual stuff
    data = s.recv(1024)
s.close()