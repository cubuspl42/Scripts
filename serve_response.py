#!/usr/bin/env python3
import http.server
import socketserver
import json

PORT = 8001
FILE_NAME = "response.json"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            with open(FILE_NAME, 'r') as f:
                file_content = json.load(f)
                http_code = file_content.get('httpCode', 200)
                self.send_response(http_code)
                file_to_open = json.dumps(file_content.get('content', {}))
        except e:
            self.send_response(500)
            self.wfile.write(bytes(str(e), 'utf-8'))

my_server = socketserver.TCPServer(("localhost", PORT), MyHttpRequestHandler)

# Start the server
print(f"Server started at localhost:{PORT}")

my_server.serve_forever()
