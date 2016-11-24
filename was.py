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
            if raw_paras[0] == 'make_vm' & len(raw_paras) == 4:
                (cmd, cpu, ram, disk) = raw_paras
                cpu = cpu.split('=')[1]
                ram = ram.split('=')[1]
                disk = disk.split('=')[1]
                self.was.create(cpu, ram, disk)
            elif raw_paras[0] == 'kill_vm' & len(raw_paras) == 2:
                (cmd, instance) = raw_paras
                instance = instance.split('=')[1]
                self.was.kill(instance)
    return MyHandler

class WebAPIServer():
    def __init__(self, dcm):
        """ WebAPIServer """
        self.dcm = dcm
        server_address = ('', 8000)
        handler = HandlerFactory(self)
        httpd = BaseHTTPServer.HTTPServer(server_address, handler)
        httpd.serve_forever()

    def create(self, cpu, ram, disk):
        req = request('c', cpu+','+ram+','+disk)
        req.sendMessage()

    def kill(self, instance):
        req = request('d', instance)
        req.sendMessage()