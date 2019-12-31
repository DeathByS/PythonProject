import socket
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(('192.168.0.40',502))

i = 0 
while i < 10:
    time.sleep(2)
    sock.send("h03h00h00h00h10".encode())
    data = sock.recv(65535)

    print("gogo", data)
