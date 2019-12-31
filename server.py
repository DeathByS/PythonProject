import socket 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('192.168.0.35',8585))

server_socket.listen(0)

client_socket, addr = server_socket.accept()

data = client_socket.recv(65535)

client_socket.send(data)

print("Recieve Data", data.decode())