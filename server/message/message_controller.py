from .fader_message import FaderMessage
from .mute_message import MuteMessage
from .message import DeskMessage

from typing import List

class MessageController():

  def __init__(self, messageInterpreters: List[DeskMessage] = []):
    self.messageInterpreters = messageInterpreters

    print(self.messageTypes)

  def add_interpreters(self, messageInterpreters: List[DeskMessage]):
    self.messageInterpreters += messageInterpreters

  def interpret_message_from_bytes(self, bytes):
    for messageType in self.messageTypes:
      if (messageType.check_bytes(bytes)):
        return messageType.from_bytes(bytes)