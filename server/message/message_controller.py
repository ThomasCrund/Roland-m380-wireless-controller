from .fader_message import FaderMessage
from .mute_message import MuteMessage
from .message import DeskMessage

from typing import List

class MessageController:

  def __init__(self, messageInterpreters: List[DeskMessage] = []):
    self.messageInterpreters = messageInterpreters

    print(self.messageInterpreters)

  def add_interpreters(self, messageInterpreters: List[DeskMessage]):
    self.messageInterpreters += messageInterpreters

  def interpret_message_from_bytes(self, bytesToCheck):
    for messageInterpreter in self.messageInterpreters:
      # print(messageInterpreter, bytesToCheck, messageInterpreter.channelProperty.check_server_type)
      if (messageInterpreter.check_bytes(bytesToCheck)):
        return messageInterpreter.from_bytes(bytesToCheck)
    raise NotImplementedError("Address: ", bytesToCheck, "not Found")
    # print("Message: ", bytesToCheck, "Is not known")