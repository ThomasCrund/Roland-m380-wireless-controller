from __future__ import annotations
import mido
from enum import Enum
from abc import ABC, abstractmethod
from typing import List

from desk.desk import Desk

class MessageDirection(Enum):
  REQUEST_HOST = 1
  SET_TO_HOST = 2
  GET_FROM_HOST = 3
  INTERPRETER = 4

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
  
  def __eq__(self, __value: object) -> bool:
    return self.bytes() == __value.bytes()
  
  def hex(self):
    output = ""
    for byte in self.bytes():
      output += hex(byte) + " "
    return output
  
  @abstractmethod
  def bytes(self):
    pass

  @abstractmethod
  def from_bytes(bytes: List[int]) -> DeskMessage:
    pass

  @abstractmethod
  def update_desk(self, desk: Desk, signalUpdate = True):
    pass
  
  @abstractmethod
  def request_update_messages(self, desk: Desk) -> List[DeskMessage]:
    pass

  @abstractmethod
  def check_bytes(self, bytes: List[int]) -> bool:
    pass

  @abstractmethod
  def check_server_type(self, type: str) -> bool:
    pass






