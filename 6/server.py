import socket
import select
import sys
from _thread import *

BUFFER_SIZE = 4096

server_address = ('127.0.0.1', 80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

threadCount = 0
input_socket = [server_socket]


try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                #start_new_thread(threaded_socket, (client_socket, ))
                #threadCount += 1
                #print(f"Thread Number: {threadCount}")
            else:
                data = sock.recv(BUFFER_SIZE).decode()
                print(data)

                request_header = data.split('\r\n')
                request_file = request_header[0].split()[1]

                if request_file == 'index.html' or request_file == '/':
                    f = open('6/index.html', 'r')
                    response_data = f.read()
                    f.close()

                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\n'
                    response_header += 'Content-type: text/html; charset=utf-8\r\n'
                    response_header += 'Content-length' + \
                        str(content_length) + '\r\n'
                    response_header += '\r\n'

                sock.sendall((response_header + response_data).encode())

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
