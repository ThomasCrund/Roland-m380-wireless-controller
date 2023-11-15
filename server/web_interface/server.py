from threading import Thread
from desk import Channel
from web_interface.channel_interface import channels_to_JSON
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random

class Server:
  
  def __init__(self, debug = False):
    # Thread.__init__(self)
    self.app = Flask(__name__)
    self.app.config['SECRET_KEY'] = 'donsky!'
    self.socketio = SocketIO(self.app, cors_allowed_origins='*')

    # self.app.debug = debug
    # self.setDaemon(True)
    # self.socketio.on('message', handler=self.handle_message)
    # self.socketio.on('my_message', handler=self.my_message)
    # self.sio.on('connect', handler=self.handle_message)
    self.threads = []

  def run(self):
    self.threads.append(self.socketio.start_background_task(self.background_task))
    self.socketio.run(self.app)

  def stop(self):
    pass

  def background_task(self):
    while True:
      self.socketio.sleep(1)
      print("background")
      self.socketio.emit('channels', { 'test': round(random() * 100)})
  
  async def send_channels(self, channels: Channel):
    await self.sio.emit('channels', channels_to_JSON(channels))

  def handle_message(self, sid, msg):
    print(sid + ' received message: ' + msg)
    self.sio.send(msg, to=sid)

  async def my_message(self, sid, data):
    await self.sio.emit('my_message', data)
    print('message ', data, sid)
