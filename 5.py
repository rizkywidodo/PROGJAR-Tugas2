import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("www.classroom.its.ac.id/my/", 80))
sock.send(b"GET / HTTP/1.1\r\nHost:www.classroom.its.ac.id/my/\r\n\r\n")
response = sock.recv(4096)
sock.close()
print(response.decode())
