import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = "classroom.its.ac.id"
sock.connect((url, 80))
sock.send(b"GET / HTTP/1.1\r\nHost:classroom.its.ac.id\r\n\r\n")
response = sock.recv(4096)

response = response.decode()
print(response)
# response = response.split("\r\n")
# content_type = response[3].split(' ')[1]
# charset = content_type.split('/')[1]

sock.close()

# BELUM