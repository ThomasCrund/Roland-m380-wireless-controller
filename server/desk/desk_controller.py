from desk.desk import Desk
from desk.desk_connection import DeskConnection
from typing import List
from message import DeskMessage
import gevent

class DeskController:

  def __init__(self, desk: Desk, deskConnection: DeskConnection):
    self.desk = desk
    self.incomingMessages: List[DeskMessage] = []
    self._listener_connected = False
    self.desk.initialise_channels()

  def run(self):
    while True:
      print("Loop")
      gevent.sleep(1)


  def add_message(self, message: DeskMessage):
    self.incomingMessages.append(message)
