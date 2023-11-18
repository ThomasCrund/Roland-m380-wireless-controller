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
    self.socketio.on_event('channel-fader-set', handler=self.set_fader)
    self.socketio.on_event('channel-mute-set', handler=self.set_mute)
    # self.socketio.on_event('my_message', handler=self.my_message)
    self.threads = []
    self.controller_callback = controller_callback

    self.channels_JSON = {}
    self.desk_connected = False
    self.client_requests = []

  def run(self):
    self.threads.append(self.socketio.start_background_task(self.background_task))
    self.socketio.run(self.app, host="0.0.0.0")

  def background_task(self):
    self.controller_callback(self)
  
  def send_channels(self, channels_JSON):
    self.channels_JSON = channels_JSON
    self.socketio.emit('channels', channels_JSON)

  def send_desk_connected(self, connected: bool):
    self.desk_connected = connected
    self.socketio.emit('desk_connected', connected)

  def handle_message(self, sid, msg):
    print(sid + ' received message: ' + msg)
    self.socketio.send(msg, to=sid)

  def set_fader(self, group, channelNum, value):
    print("Set Fader", group, channelNum, value)
    self.client_requests.append({ 'type': 'channel-fader-set', 'group': group, 'channelNum': channelNum, 'value': value})

  def set_mute(self, group, channelNum, value):
    print("Set mute", group, channelNum, value)
    self.client_requests.append({ 'type': 'channel-mute-set', 'group': group, 'channelNum': channelNum, 'value': value})

  def connect(self):
    print("new connection", request.args)
    self.socketio.emit('channels', self.channels_JSON)
    self.socketio.emit('desk_connected', self.desk_connected)
    
