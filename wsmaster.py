
# from tornado import *
from tornado.websocket import WebSocketHandler
import tornado
import tornado.web

import simplejson as json

class WSHandler(WebSocketHandler):
    
    def check_origin(self, origin):
        return True

    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        self.write_message("You said " + message)

    def on_close(self):
        print "Connection closed"


app = tornado.web.Application([
        (r"/socket", WSHandler)
    ])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

