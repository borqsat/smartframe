#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()  # monkey patch for gevent

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler
from bottle import Bottle, static_file, redirect
import os

from smartserver.config import WEB_HOST, WEB_PORT  # import db configuration and arguments
from smartserver.liveapis import appws as ws
from smartserver.groupapis import appweb as api

app = Bottle()


@app.route("/smartserver/<filename:path>")
def assets(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web'))


@app.route("/")
@app.route("/smartserver")
@app.route("/smartserver/")
def root():
    return redirect("/smartserver/index.html")


api.mount('/ws', ws)
app.mount('/smartapi', api)


def main():
    port = WEB_PORT
    host = WEB_HOST
    print 'Smartserver Serving on %s:%d...' % (host, port)
    WSGIServer(("", port), app, handler_class=WebSocketHandler).serve_forever()

if __name__ == '__main__':
    main()
