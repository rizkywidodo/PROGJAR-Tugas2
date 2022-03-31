import socket
import select
import sys
import os
import threading
import time

f = open('6/server/httpserver.conf', 'r')
port = int(f.read())
f.close()

server_address = ('127.0.0.1', port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(10)

input_socket = [server_socket]
threads = []

def worker(sock):
    while True:
        data = sock.recv(1024).decode()
        print(data)

        request_header = data.split('\r\n')
        request_path = request_header[0].split()[1]
        response_header = ''
        response_data = ''
        
        if request_path == '/index.html' or request_path == '/':
            
            f = open('6/server/index.html', 'r')
            response_data = f.read()
            f.close()

            content_length = len(response_data)
            response_header = 'HTTP/1.0 200 OK\r\n'
            response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
            response_header += 'Content-Length: ' + str(content_length)  + '\r\n'
            response_header += '\r\n'

        elif request_path =='/directory':
            response_data = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Directory</title>
            </head>
            <body>
                <h1>Index of directory</h1>
            '''
            for root, dirs, files in os.walk("6/server/dataset", topdown=False):
                for name in files:
                    response_data += '''
                        <div>
                        File: {}
                        </div>
                    '''.format(name)
                for name in dirs:
                    response_data += '''
                        <div>
                        Folder: {}
                        </div>
                    '''.format(name)
            response_data += '''
            </body>
            </html>
            '''

            content_length = len(response_data)
            response_header = 'HTTP/1.0 200 OK\r\n'
            response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
            response_header += 'Content-Length: ' + str(content_length)  + '\r\n'
            response_header += '\r\n'
        
        else:
            if os.path.exists(f"6/server/dataset{request_path}"):
                f = open(f"6/server/dataset{request_path}", 'rb')
                while True:
                    bytes_read = f.read(4096)
                    if not bytes_read:
                        break
                    sock.sendall(bytes_read)
                f.close()
                client_socket.close()
                input_socket.remove(sock)
                print(f"File {request_path} has been sent!")
                print(f"client Disconnected!\n")
                break
                
            else:
                f = open('6/server/404.html', 'r')
                response_data = f.read()
                f.close()
                content_length = len(response_data)
                response_header = 'HTTP/1.0 404 Not Found\r\n'
                response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
                response_header += 'Content-Length: ' + str(content_length)  + '\r\n'
                response_header += '\r\n'

        sock.sendall((response_header + response_data).encode())
        client_socket.close()
        input_socket.remove(sock)
        break
try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                t = threading.Thread(target=worker, args=(client_socket,))
                threads.append(t)
                t.start()
                time.sleep(10)
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
