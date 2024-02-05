from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from desk.desk import Desk
from typing import List

deviceId = 0x10
modelId = [0x00, 0x00, 0x24]

class SysExcMessage(DeskMessage):

  def __init__(self, address: List[int], data: List[int], size: List[int], messageType: MessageType, direction: MessageDirection = MessageDirection.SET_TO_HOST):
    super().__init__(direction, messageType)
    self.address: List[int] = address
    self.data: List[int] = data
    self.size: List[int] = size


  def bytes(self):
    bytes = []
    if self.dir == MessageDirection.SET_TO_HOST or self.dir == MessageDirection.GET_FROM_HOST:
      bytes.append(0xF0) # Start Byte
      bytes.append(0x41) # Manufacture ID
      bytes.append(deviceId)
      bytes += modelId
      bytes.append(0x12) # Command Id
      bytes += self.address
      bytes += self.data
      bytes.append(calculate_checksum(self.address + self.data))
      bytes.append(0xF7)
    elif self.dir == MessageDirection.REQUEST_HOST:
      bytes.append(0xF0) # Start Byte
      bytes.append(0x41) # Manufacture ID
      bytes.append(deviceId)
      bytes += modelId
      bytes.append(0x11) # Command Id
      bytes += self.address
      bytes += self.size
      bytes.append(calculate_checksum(self.address + self.size))
      bytes.append(0xF7)
    return bytes
  
  def from_bytes(self, bytes: List[int]) -> SysExcMessage:
    print("### from bytes Not Implemented (SysExc message)")

  def update_desk(self, desk: Desk):
    print("### update desk Not Implemented (SysExc message)")

  def update_message(self) -> SysExcMessage | None:
    return SysExcMessage(self.address, [0, 0, 0, 0], self.size, self.messageType, MessageDirection.REQUEST_HOST)

  def request_update_messages(self, desk: Desk) -> List[DeskMessage]:
    print("### request_update_messages Not Implemented (SysExc message)")
    return []

  def check_bytes(self, bytes: List[int]) -> bool:
    if len(bytes) < 5: return False
    if bytes[0] != 0xF0:
      return False
    if bytes[1] != 0x41:
      return False
    if bytes[2] != deviceId:
      return False
    if bytes[3] != modelId[0] or bytes[4] != modelId[1] or bytes[5] != modelId[2]:
      return False
    if bytes[6] != 0x12:
      return False
    # bytes[7:10] == address
    # bytes[11:14] == data
    if bytes[-2] != calculate_checksum(bytes[7:-2]):
      print(bytes[-2], calculate_checksum(bytes[7:-2]))
      return False
    if bytes[-1] != 0xF7:
      return False
    return True
  
  def check_server_type(self, type: str) -> bool:
    return type == "fader"
    
def calculate_checksum(data: List[int]):
  sum = 0
  for byte in data:
    sum += byte
  odd = sum % 128
  if odd == 0:
    return 0
  else:
    return 128 - odd