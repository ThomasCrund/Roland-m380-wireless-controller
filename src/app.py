from server import Server
from desk import Desk
from interface import Listener
import time

class App:

  def __init__(self):
    self.server = Server()
    self.desk = Desk()
    self.listener = Listener(self.desk, "test")

  def run(self):
    print("Starting App")
    self.server.start()
    self.listener.start()
    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      print("End Logger")

  def exit_application(self, num, stack):
    print("Closing App")
    # self.server.end()
    exit()



    