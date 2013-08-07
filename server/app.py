#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()  # monkey patch for gevent

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler
from bottle import Bottle, static_file, redirect
import os

from smartserver.config import WEB_HOST, WEB_PORT  # import db configuration and arguments
from smartserver.api import v0


# Below code is to fix known log issue because of mismatch on gevent and gunicorn
# http://stackoverflow.com/questions/9444405/gunicorn-and-websockets
def log_request(self):
    log = self.server.log
    if log:
        if hasattr(log, "info"):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')

import gevent
gevent.pywsgi.WSGIHandler.log_request = log_request
# end of fix

app = Bottle()


@app.route("/smartserver/<filename:path>")
def assets(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web'))


@app.route("/")
@app.route("/smartserver")
@app.route("/smartserver/")
def root():
    return redirect("/smartserver/index.html")

@app.route("/report/<token>")
def report(token):
    return redirect("/smartserver/report.html#reportsnapshot/"+token+"")

app.mount('/smartapi', v0)
app.mount('/smart/0/api/', v0)


def main():
    port = WEB_PORT
    host = WEB_HOST
    print 'Smartserver Serving on %s:%d...' % (host, port)
    WSGIServer(("", port), app, handler_class=WebSocketHandler).serve_forever()

if __name__ == '__main__':
    main()
