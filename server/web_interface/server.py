from threading import Thread
# from web_interface.channel_interface import channels_to_JSON
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from random import random
from web_interface.user_controller import UserController

class Server:
  
  def __init__(self, controller_callback, debug = False):
    # Thread.__init__(self)
    self.app = Flask(__name__)
    self.app.config['SECRET_KEY'] = 'donsky!'
    self.socketio = SocketIO(self.app, cors_allowed_origins='*', logger=debug, engineio_logger=debug)

    self.socketio.on_event('message', handler=self.handle_message)
    self.socketio.on_event('connect', handler=self.connect)
    self.socketio.on_event('channel-set', handler=self.set_channel_property)
    self.socketio.on_event('input-set', handler=self.set_input_property)
    # self.socketio.on_event('my_message', handler=self.my_message)
    self.threads = []
    self.controller_callback = controller_callback

    self.listsJSON = {}
    self.desk_connected = False
    self.client_requests = []
    self.user_controller = UserController()

  def run(self):
    self.threads.append(self.socketio.start_background_task(self.background_task))
    self.socketio.run(self.app, host="0.0.0.0")

  def background_task(self):
    self.controller_callback(self)
  
  def send_list(self, list_name, channels_JSON, sid_to_exclude = ""):
    self.listsJSON[list_name] = channels_JSON
    sids = self.user_controller.getSidsMinusOne(sid_to_exclude)
    for sid in sids:
      self.socketio.emit(list_name, channels_JSON, to=sid)

  def send_desk_connected(self, connected: bool):
    self.desk_connected = connected
    self.socketio.emit('desk_connected', connected)

  def handle_message(self, sid, msg):
    print(sid + ' received message: ' + msg)
    self.socketio.send(msg, to=sid)

  def set_channel_property(self, property, group, channelNum, value, update_itself = False):
    print("Set channel " + property, group, channelNum, value, request.sid)
    self.client_requests.append({ 'type': 'channel', 'property': property, 'group': group, 'channelNum': channelNum, 'value': value, 'update_itself': update_itself, 'user': request.sid})

  def set_input_property(self, property, inputSource, inputNumber, value, update_itself = False):
    print("Set input " + property, inputSource, inputNumber, value, request.sid)
    self.client_requests.append({ 'type': 'input', 'property': property, 'inputSource': inputSource, 'inputNumber': inputNumber, 'value': value, 'update_itself': update_itself, 'user': request.sid})

  def connect(self):
    print("new connection", request.sid, self.user_controller.getSidsMinusOne(""))
    self.user_controller.addUser(request.sid)
    print("new connection", request.sid, self.user_controller.getSidsMinusOne(""))
    for listName in self.listsJSON:
      self.socketio.emit(listName, self.listsJSON[listName], to=request.sid)
    self.socketio.emit('desk_connected', self.desk_connected)
    
