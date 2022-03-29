import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = "its.ac.id"
sock.connect((url, 80))
sock.send(b"GET / HTTP/1.1\r\nHost:www.its.ac.id\r\n\r\n")
response = sock.recv(4096)
response = response.decode()
response = response.split("\r\n")
ver = response[0].split(' ')[0]
print(ver)

sock.close()