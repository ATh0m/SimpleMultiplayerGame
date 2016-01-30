import socket
import sys
import time
import pickle

host = 'localhost'
port = 1234
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while 1:
    line = pickle.dumps(('TIME', time.ctime(time.time())))
    s.send(line)
    data = s.recv(size)
    data = pickle.loads(data)
    print(data)

s.close()
