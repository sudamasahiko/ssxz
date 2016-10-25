# -*- coding:utf-8 -*-

# 
# was.py
# 

import BaseHTTPServer
import json

def HandlerFactory(was):
    class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            self.was = was
            BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-Type', 'text/json')
            self.end_headers()
            responseData = json.dumps({'spam': self.was.ack()})
            self.wfile.write(responseData.encode('UTF-8'))

    return MyHandler

class WebAPIServer():
    def __init__(self):
        """ WebAPIServer """
        self.ham = 'ham'
        server_address = ('', 8000)
        handler = HandlerFactory(self)
        httpd = BaseHTTPServer.HTTPServer(server_address, handler)
        httpd.serve_forever()

    def ack(self):
        return 'ham'