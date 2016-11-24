# -*- coding:utf-8 -*-

# 
# ssxz_daemon.py
# 

import sys
import time
import BaseHTTPServer
from daemon import Daemon
from ssxz import Ssxz

class YourCode(object):
    def run(self):
        self.ssxz = Ssxz()
        while True:
            time.sleep(1)


class MyDaemon(Daemon):
    def run(self):
        your_code = YourCode()
        your_code.run()


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-ssxz.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)