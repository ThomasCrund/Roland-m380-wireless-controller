from threading import Thread
import socketio
from aiohttp import web
from desk import Channel
from web_interface.channel_interface import channels_to_JSON

import time

class Server:
  
  def __init__(self, debug = False):
    # Thread.__init__(self)
    self.sio = socketio.AsyncServer(logger=True, cors_allowed_origins='*')
    self.debug = debug
    # self.app.debug = debug
    # self.setDaemon(True)
    self.sio.on('message', handler=self.handle_message)
    self.sio.on('my_message', handler=self.my_message)
    # self.sio.on('connect', handler=self.handle_message)
    self.app = web.Application()
    self.sio.attach(self.app)

  def run(self):
    web.run_app(self.init_app())

  def stop(self):
    pass

  def test_task(self):
    print("background")

  async def init_app(self):
    self.sio.start_background_task(self.test_task)
    return self.app
  
  async def send_channels(self, channels: Channel):
    await self.sio.emit('channels', channels_to_JSON(channels))

  def handle_message(self, sid, msg):
    print(sid + ' received message: ' + msg)
    self.sio.send(msg, to=sid)

  async def my_message(self, sid, data):
    await self.sio.emit('my_message', data)
    print('message ', data, sid)
