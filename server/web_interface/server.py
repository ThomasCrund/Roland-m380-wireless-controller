from threading import Thread
# from web_interface.channel_interface import channels_to_JSON
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from random import random

class Server:
  
  def __init__(self, controller_callback, debug = False):
    # Thread.__init__(self)
    self.app = Flask(__name__)
    self.app.config['SECRET_KEY'] = 'donsky!'
    self.socketio = SocketIO(self.app, cors_allowed_origins='*', logger=debug, engineio_logger=debug)

    self.socketio.on_event('message', handler=self.handle_message)
    self.socketio.on_event('connect', handler=self.connect)
    self.socketio.on_event('channel-set', handler=self.set_channel_property)
    # self.socketio.on_event('my_message', handler=self.my_message)
    self.threads = []
    self.controller_callback = controller_callback

    self.listsJSON = {}
    self.desk_connected = False
    self.client_requests = []

  def run(self):
    self.threads.append(self.socketio.start_background_task(self.background_task))
    self.socketio.run(self.app, host="0.0.0.0")

  def background_task(self):
    self.controller_callback(self)
  
  def send_list(self, list_name, channels_JSON):
    self.listsJSON[list_name] = channels_JSON
    self.socketio.emit(list_name, channels_JSON)

  def send_desk_connected(self, connected: bool):
    self.desk_connected = connected
    self.socketio.emit('desk_connected', connected)

  def handle_message(self, sid, msg):
    print(sid + ' received message: ' + msg)
    self.socketio.send(msg, to=sid)

  def set_channel_property(self, property, group, channelNum, value, update_itself = False):
    print("Set" + property, group, channelNum, value)
    self.client_requests.append({ 'type': 'channel', 'property': property, 'group': group, 'channelNum': channelNum, 'value': value, 'update_itself': update_itself})

  def connect(self):
    print("new connection", request.args)
    for listName in self.listsJSON:
      self.socketio.emit(listName, self.listsJSON[listName])
    self.socketio.emit('desk_connected', self.desk_connected)
    
