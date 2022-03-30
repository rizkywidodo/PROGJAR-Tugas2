import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = "its.ac.id"
sock.connect((url, 80))
sock.send(b"GET / HTTP/1.1\r\nHost:its.ac.id\r\n\r\n")
response = sock.recv(4096)

response = response.decode()
#print(response)
response = response.split("\r\n")
status = response[0].split('HTTP/1.1 ')[1]
print(status)

sock.close()

# DONE