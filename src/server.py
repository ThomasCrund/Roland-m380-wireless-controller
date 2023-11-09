from threading import Thread
from flask import Flask

import time

class Server(Thread):
  
  def __init__(self, debug = False):
    Thread.__init__(self)
    self.app = Flask(__name__)
    self.debug = debug
    self.app.debug = debug
    self.setDaemon(True)

  def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
    self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

  def run(self):
    self.app.run()


  def stop(self):
    pass