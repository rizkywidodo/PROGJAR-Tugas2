import socket
import sys
import os
from bs4 import BeautifulSoup

try:
    while True:
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        url = '127.0.0.1'
        server_address = (url, 80)
        client_socket.connect(server_address)
        
        message = sys.stdin.readline()
        message = message.rstrip()
        print(message)
        
        if message.split()[0] == 'index.html':
            
            request_header = 'GET /index.html HTTP/1.0\r\n'
            request_header += 'Host: ' + url + '\r\n'
            request_header += '\r\n'

            client_socket.send(request_header.encode())

            response = ''
            
            while True:
                recv = client_socket.recv(1024).decode()
                if not recv: 
                    break
                response += recv

            soup = BeautifulSoup(response, 'html.parser')
            print(soup.get_text())
            client_socket.close()
        
        elif message.split()[0] == 'directory':
        
            request_header = 'GET /directory HTTP/1.0\r\n'
            request_header += 'Host: ' + url + '\r\n'
            request_header += '\r\n'

            client_socket.send(request_header.encode())

            response = ''

            while True:
                recv = client_socket.recv(1024).decode()
                if not recv: 
                    break
                response += recv

            soup = BeautifulSoup(response, 'html.parser')
            print(soup.get_text())
            client_socket.close()
            
        elif message.split()[0] == 'download':
            
            filename = message.split(" ")[1]
            
            try:
                os.remove(filename)
            except:
                None
            
            request_header = 'GET /' + filename + ' HTTP/1.0\r\n'
            request_header += 'Host: ' + url + '\r\n'
            request_header += '\r\n'
            
            client_socket.send(request_header.encode())
            
            response = ''
            filename = '6/client/' + filename
            
            f = open(filename, 'wb')
            while True:
                bytes_read = client_socket.recv(4096)
                if not bytes_read: 
                    break
                f.write(bytes_read)
            f.close()
            client_socket.close()
            
        else:
            
            request_header = 'GET /' + message + ' HTTP/1.0\r\n'
            request_header += 'Host: ' + url + '\r\n'
            request_header += '\r\n'

            client_socket.send(request_header.encode())

            response = ''

            while True:
                recv = client_socket.recv(1024).decode()
                if not recv: 
                    break
                response += recv

            soup = BeautifulSoup(response, 'html.parser')
            print(soup.get_text())
            client_socket.close()
            
except KeyboardInterrupt:
    client_socket.close()