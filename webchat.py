
import os
from datetime import datetime
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape


class Clients():
    ids = {}
    sockets = {}

    def add_client(self, id, socket):
        self.ids[str(id)] = socket
        self.sockets[socket] = str(id)

    def get_id(self, socket):
        return self.sockets[socket] if socket in self.sockets else None

    def get_socket(self, id):
        return self.ids[str(id)] if str(id) in self.ids else None

    def get_all_sockets(self):
        return self.sockets.keys()

    def remove_client(self, socket):
        del self.ids[self.sockets[socket]]
        del self.sockets[socket]

clients = Clients()

class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")

class WebChatHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        print 'check_origin', self, origin
        return True

    def open(self, client_id):
        print 'open', self, client_id
        clients.add_client(client_id, self)
        print clients.ids

    def on_message(self, message):
        message = tornado.escape.json_decode(message)
        print 'message', self, message

        from_id = clients.get_id(self)

        message_to_be_sent = {
            'from': from_id,
            'message': message['message'],
            'created_at': datetime.now().isoformat(),
        }

        if 'to' in message and message['to']:
            #one to one chat
            to_socket = clients.get_socket(message['to'])

            self.write_message(message_to_be_sent)
            to_socket.write_message(message_to_be_sent)

    def on_close(self):
        print 'close', self
        clients.remove_client(self)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/webchat/(.*?)$', WebChatHandler),
        (r'/(.+?\.js)$', tornado.web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
        (r'/', IndexHandler),
    ])

    app.listen(7200)
    tornado.ioloop.IOLoop.instance().start()
