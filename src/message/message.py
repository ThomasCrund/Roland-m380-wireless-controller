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
  CHANNEL = 1
  INPUT_PATCHBAY = 2
  OUTPUT_PATCHBAY = 3
  RECORDING = 4
  MUTE_GROUP = 5
  MONITOR = 6
  DCA_GROUP = 7
  TALKBACK = 8

class DeskMessage(ABC):
  def __init__(self, dir: MessageDirection, type: MessageType):
    self.dir = dir
    self.type = type

  def get_msg(self):
    return mido.Message.from_bytes(bytes)
  
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






