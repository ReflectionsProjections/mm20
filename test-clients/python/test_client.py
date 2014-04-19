import socket

HOST = 'localhost'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('{"team":"test", "members":[{"name":"test1", "class":"Coder"},{"name":"test2", "class":"Coder"},{"name":"test3", "class":"Coder"}]}')
data = s.recv(1024)
while len(data) > 0: #TODO: Need check for game over
    print 'Received', repr(data)
    s.sendall('[{"action":"dummy"}]')
    data = s.recv(1024)
s.close()