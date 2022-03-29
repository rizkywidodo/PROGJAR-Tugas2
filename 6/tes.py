request_header = ['GET /index.html HTTP/1.0', 'test']
request_path = request_header[0].split()[1]

print(request_path)