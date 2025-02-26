from web_interface.server import Server
from desk.desk_controller import DeskController
from desk.desk_connection import DeskConnection
from desk.desk import Desk
import time
import asyncio

class App:

  def __init__(self):
    self.desk = Desk()
    self.deskConnection = DeskConnection("M-380 MIXING CONSOLE:M-380 MIXING CONSOLE MIDI 1 28:0", "M-380 MIXING CONSOLE:M-380 MIXING CONSOLE MIDI 1 28:0", debug=3)
    self.deskController = DeskController(self.desk, self.deskConnection)
    self.server: Server = Server(self.deskController.run)

  def run(self):
    print("Starting App")
    self.server.run()
    
  def exit_application(self, num, stack):
    print("Closing App")
    # self.server.end()
    exit()



    