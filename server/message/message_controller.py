from .fader_message import FaderMessage
from .mute_message import MuteMessage
from .message import DeskMessage
from desk.desk import Desk

from typing import List

class MessageController:

  def __init__(self, messageInterpreters: List[DeskMessage] = []):
    self.messageInterpreters = messageInterpreters

    print(self.messageInterpreters)

  def add_interpreters(self, messageInterpreters: List[DeskMessage]):
    self.messageInterpreters += messageInterpreters

  def interpret_message_from_bytes(self, bytesToCheck):
    for messageInterpreter in self.messageInterpreters:
      if (messageInterpreter.check_bytes(bytesToCheck)):
        return messageInterpreter.from_bytes(bytesToCheck)
    raise NotImplementedError("Address: ", bytesToCheck, "not Found")
  
  def request_update_messages(self, desk: Desk):
    messages: List[DeskMessage] = []
    for messageInterpreter in self.messageInterpreters:
      messages += messageInterpreter.request_update_messages(desk)
    return messages