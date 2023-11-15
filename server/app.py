from web_interface import Server
from desk import Desk, DeskController, DeskConnection
import time
import asyncio
import gevent

class App:

  def __init__(self):
    self.server: Server = Server()
    self.desk = Desk()
    self.deskConnection = DeskConnection("2- RSS M-400 0", "2- RSS M-400 1")
    self.deskController = DeskController(self.desk, self.deskConnection)

  def run(self):
    print("Starting App")
    # self.server.start_background_task(self.deskController.run)
    self.server.run()
    

  def exit_application(self, num, stack):
    print("Closing App")
    # self.server.end()
    exit()



    