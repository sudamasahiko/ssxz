# -*- coding:utf-8 -*-

# 
# was.py
import BaseHTTPServer
import json

def HandlerFactory(was):
    class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            self.was = was
            BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

        def do_GET(self):
            '''
            request = urllib.parse.urlparse(self.path)
            params = dict(urllib.parse.parse_qsl(request.query))

            # レスポンスを生成
            body = self.body(request.path, params)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-length', len(body))
            self.end_headers()
            self.wfile.write(body)
            '''
            self.send_response(200)
            self.send_header('Content-Type', 'text/json')
            self.end_headers()
            responseData = self.path.split('=')[1]
            if self.path.split('=')[1] == 'make_vm':
                #条件あっていれば、以下のスプリントを開始する
                #os.sys('****.py')
                self.wfile.write(responseData)
            '''
            if self.path.split('=')[1] == 'make_vm':
                print 'ok'
            #print responseDate
            #json.dumps({'spam': 'spam'})
            self.wfile.write(responseData.encode('UTF-8'))
            responseData = self.path.split('&')[1]
            '''
            #self.wfile.write(responseData)


    return MyHandler

class WebAPIServer():
    def __init__(self):
        """ WebAPIServer """
        self.ham = 'ham'
        #self.dcm = dcm
        server_address = ('', 8000)
        handler = HandlerFactory(self)
        httpd = BaseHTTPServer.HTTPServer(server_address, handler)
        httpd.serve_forever()

    def ack(self):
        return 'ham'
