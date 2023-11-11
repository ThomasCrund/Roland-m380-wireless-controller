from server import Server
from desk import Desk, DeskController, DeskConnection
import time

class App:

  def __init__(self):
    self.server = Server()
    self.desk = Desk()
    self.deskConnection = DeskConnection("2- RSS M-400 0", "2- RSS M-400 1")
    self.deskController = DeskController(self.desk, self.deskConnection)

  def run(self):
    print("Starting App")
    self.server.start()
    try:
      while True:
        self.deskConnection.update()
        time.sleep(1)
    except KeyboardInterrupt:
      print("End Logger")

  def exit_application(self, num, stack):
    print("Closing App")
    # self.server.end()
    exit()



    