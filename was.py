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
            cmd = raw_paras[0].split('=')[1]
            if cmd == 'make_vm' and len(raw_paras) == 4:
                (cmd, cpu, ram, disk) = raw_paras
                cpu = cpu.split('=')[1]
                ram = ram.split('=')[1]
                disk = disk.split('=')[1]
                self.was.create(cpu, ram, disk)
            elif cmd == 'kill_vm' and len(raw_paras) == 2:
                (cmd, instance) = raw_paras
                instance = instance.split('=')[1]
                self.was.kill(instance)
    return MyHandler

class WebAPIServer():
    def __init__(self):
        """ WebAPIServer """
        server_address = ('192.168.122.3', 8000)
        handler = HandlerFactory(self)
        httpd = BaseHTTPServer.HTTPServer(server_address, handler)
        httpd.serve_forever()

    def create(self, cpu, ram, disk):
        # print('c', cpu+','+ram+','+disk)
        params = cpu+','+ram+','+disk
        req = request.request('c', params)
        print('requesting '+params)
        ret = req.sendMessage()
        print('requested. instance id: '+str(ret))

    def kill(self, instance):
        # print('d', instance)
        req = request.request('d', instance)
        req.sendMessage()
