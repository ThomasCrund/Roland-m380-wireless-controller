from desk import Desk
from typing import List
from message import DeskMessage

class DeskController:

  def __init__(self, desk: Desk):
    self.desk = desk
    self.incomingMessages: List[DeskMessage] = []

  def add_message(self, message: DeskMessage):
    self.incomingMessages.append(message)