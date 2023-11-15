from threading import Thread
import socketio
import eventlet

import time

class Server(Thread):
  
  def __init__(self, debug = False):
    Thread.__init__(self)
    self.sio = socketio.Server(logger=True, cors_allowed_origins='*')
    self.debug = debug
    # self.app.debug = debug
    self.setDaemon(True)
    self.sio.on('message', handler=self.handle_message)
    self.sio.on('my_message', handler=self.my_message)
    # self.sio.on('connect', handler=self.handle_message)
    self.app = socketio.WSGIApp(self.sio)

  def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
    # self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)
    pass

  def run(self):
    eventlet.wsgi.server(eventlet.listen(('', 5000)), self.app)
    print("test")

  def stop(self):
    pass

  def send_channel(self):
    self.sio.send('test')
    # self.sio.emit('faders', { 'channels': [ { 'group': 'FADER', 'channel': 1, 'mute': False, 'volume': 60 }]})

  def handle_message(self, sid, msg):
    print(sid + ' received message: ' + msg)
    self.sio.send(msg, to=sid)

  def my_message(self, sid, data):
    self.sio.emit('my_message', data)
    print('message ', data)