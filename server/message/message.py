import mido
from enum import Enum
from abc import ABC, abstractmethod
from typing import List

from desk import Desk

class MessageDirection(Enum):
  REQUEST_HOST = 1
  SET_TO_HOST = 2
  GET_FROM_HOST = 3

class MessageType(Enum):
  CHANNEL = "CHANNEL"
  INPUT_PATCHBAY = "INPUT_PATCHBAY"
  OUTPUT_PATCHBAY = "OUTPUT_PATCHBAY"
  RECORDING = "RECORDING"
  MUTE_GROUP = "MUTE_GROUP"
  MONITOR = "MONITOR"
  DCA_GROUP = "DCA_GROUP"
  TALKBACK = "TALKBACK"

class DeskMessage(ABC):
  def __init__(self, dir: MessageDirection, messageType: MessageType):
    self.dir = dir
    self.messageType = messageType

  def get_msg(self):
    return mido.Message.from_bytes(self.bytes())
  
  @abstractmethod
  def bytes(self):
    pass

  def hex(self):
    output = ""
    for byte in self.bytes():
      output += hex(byte) + " "
    return output

  @abstractmethod
  def from_bytes(bytes: List[int]):
    pass

  @abstractmethod
  def update_desk(self, desk: Desk):
    pass






