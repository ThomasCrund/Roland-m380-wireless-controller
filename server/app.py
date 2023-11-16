from web_interface import Server
from desk import Desk, DeskController, DeskConnection
import time
import asyncio

class App:

  def __init__(self):
    self.desk = Desk()
    self.deskConnection = DeskConnection("RSS M-400 0", "RSS M-400 1")
    self.deskController = DeskController(self.desk, self.deskConnection)
    self.server: Server = Server(self.deskController.run)

  def run(self):
    print("Starting App")
    self.server.run()
    
  def exit_application(self, num, stack):
    print("Closing App")
    # self.server.end()
    exit()



    