# -*- coding:utf-8 -*-

#
# was.py
import BaseHTTPServer
import json
import request

def HandlerFactory(was):
    class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def __init__(self, req, client_address, server):
            self.was = was
            BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, req, client_address, server)

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-Type', 'text/json')
            self.end_headers()
            raw_paras = self.path.split('?')[1].split('&')
            paras = {}
            for p in raw_paras:
                buf = p.split('=')
                paras[buf[0]] = buf[1]

            if not 'cmd' in paras:
                self.wfile.write('ng')
                return

            if paras['cmd'] == 'make_vm':
                if len(paras) == 4 and 'cpu' in paras and 'ram' in paras and 'disk' in paras:
                    self.was.create(paras['cpu'], paras['ram'], paras['disk'])
                    self.wfile.write('ok')
                else:
                    self.wfile.write('ng')
            elif paras['cmd'] == 'kill_vm':
                if len(paras) == 2 and 'id' in paras:
                    self.was.kill(paras['id'])
                else:
                    self.wfile.write('ng')
            else:
                self.wfile.write('ng')
    return MyHandler

class WebAPIServer():
    def __init__(self):
        """ WebAPIServer """
        ip = '192.168.122.3'
        port = 8000
        server_address = (ip, port)
        handler = HandlerFactory(self)
        httpd = BaseHTTPServer.HTTPServer(server_address, handler)
        httpd.serve_forever()

    def create(self, cpu, ram, disk):
        params = cpu + ',' + ram + ',' + disk
        req = request.request('c', params)
        print('requesting ' + params)
        ret = req.sendMessage()
        print('requested. instance id: '+str(ret))

    def kill(self, instance):
        req = request.request('d', instance)
        req.sendMessage()
