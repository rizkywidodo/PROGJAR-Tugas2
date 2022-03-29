import socket
import select
import sys
import os

server_address = ('127.0.0.1', 80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            
            else:
                data = sock.recv(1024).decode()
                print(data)

                request_header = data.split('\r\n')[0]
                temp = request_header.split()
                request_path = temp[1]
                response_header = ''
                response_data = ''
                print(f"ini {len(temp)}")
                if request_path == '/index.html' or request_path == '/':
                    try:
                        f = open('6/index.html', 'r')
                        response_data = f.read()
                        f.close()

                        content_length = len(response_data)
                        response_header = 'HTTP/1.0 200 OK\r\n'
                        response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
                        response_header += 'Content-Length: ' + str(content_length)  + '\r\n'
                        response_header += '\r\n'

                    except IOError:
                        response_data = '''
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Halo Ngab!</title>
                        </head>
                        <body>
                            <h1>Index of directory</h1>
                        '''
                        for root, dirs, files in os.walk("6/dataset", topdown=False):
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

                sock.sendall((response_header + response_data).encode())

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
