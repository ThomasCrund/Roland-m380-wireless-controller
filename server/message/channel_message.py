from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from message.sysexc_message import SysExcMessage
from desk.desk import Desk
from typing import List
from enum import Enum

class ChannelProperty():
  def __init__(self, address, size, check_server_type, data_range: (int, int) = (0, 127)):
    self.address = address
    self.size = size
    self.check_server_type = check_server_type
    self.data_range = data_range

class ChannelProperties(Enum):
  NAME = ChannelProperty([0x00, 0x00], 6, "name")
  NAME_COLOR = ChannelProperty([0x00, 0x06], 1, "name_color", (0, 7))
  LINK = ChannelProperty([0x00, 0x08], 1, "link", (0, 1))
  PHASE = ChannelProperty([0x00, 0x09], 1, "phase", (0, 1))
  ATT = ChannelProperty([0x00, 0x0A], 2, "att")
  MUTE = ChannelProperty([0x00, 0x0C], 1, "mute", (0, 1))
  SOLO = ChannelProperty([0x00, 0x0D], 1, "solo", (0, 1))
  FADER = ChannelProperty([0x00, 0x0E], 2, "fader")
  PAN = ChannelProperty([0x00, 0x10], 1, "pan", (1, 0x7F))
  MAIN_SWITCH = ChannelProperty([0x00, 0x11], 1, "main_switch", (0, 1))
  
  FILTER_SWITCH = ChannelProperty([0x00, 0x20], 1, "filter_switch", (0, 1))
  FILTER_TYPE = ChannelProperty([0x00, 0x21], 1, "filter_type", (0, 3))
  FILTER_ATT = ChannelProperty([0x00, 0x22], 2, "filter_att", (0, 0x7F))
  FILTER_FREQ = ChannelProperty([0x00, 0x24], 3, "filter_freq", (0, 0x7f))
  FILTER_Q = ChannelProperty([0x00, 0x27], 2, "filter_q", (0, 0x7f))
  
  GATE_SWITCH = ChannelProperty([0x00, 0x30], 1, "gate_switch", (0, 1))
  GATE_KEY_IN = ChannelProperty([0x00, 0x31], 1, "gate_key_in")
  GATE_MODE = ChannelProperty([0x00, 0x32], 1, "gate_mode", (0, 2))
  GATE_THRESHOLD = ChannelProperty([0x00, 0x33], 2, "gate_threshold")
  GATE_RATIO = ChannelProperty([0x00, 0x35], 1, "gate_ratio", (0, 0x0d))
  GATE_KNEE = ChannelProperty([0x00, 0x36], 1, "gate_knee", (0, 9))
  GATE_RANGE = ChannelProperty([0x00, 0x37], 2, "gate_range")
  GATE_ATTACK = ChannelProperty([0x00, 0x39], 2, "gate_attack")
  GATE_RELEASE = ChannelProperty([0x00, 0x3B], 2, "gate_release")
  GATE_HOLD = ChannelProperty([0x00, 0x3D], 2, "gate_hold")

  COMP_SWITCH = ChannelProperty([0x00, 0x40], 1, "comp_switch", (0, 1))
  COMP_KEY_IN = ChannelProperty([0x00, 0x41], 1, "comp_key_in")
  COMP_THRESHOLD = ChannelProperty([0x00, 0x42], 2, "comp_threshold")
  COMP_RATIO = ChannelProperty([0x00, 0x44], 1, "comp_ratio", (0, 0x0d))
  COMP_KNEE = ChannelProperty([0x00, 0x45], 1, "comp_knee", (0, 9))
  COMP_ATTACK = ChannelProperty([0x00, 0x46], 2, "comp_attack")
  COMP_RELEASE = ChannelProperty([0x00, 0x48], 2, "comp_release")
  COMP_GAIN = ChannelProperty([0x00, 0x4A], 2, "comp_hold")
  COMP_AUTO_GAIN = ChannelProperty([0x00, 0x4C], 1, "comp_switch", (0, 1))

  EQ_SWITCH = ChannelProperty([0x00, 0x50], 1, "eq_switch", (0, 1))
  EQ_ATT = ChannelProperty([0x00, 0x51], 2, "eq_att")
  EQ_LO_GAIN = ChannelProperty([0x00, 0x51], 2, "eq_att")
  EQ_LO_FREQ = ChannelProperty([0x00, 0x51], 2, "eq_att")
  EQ_ATT = ChannelProperty([0x00, 0x51], 2, "eq_att")
  EQ_ATT = ChannelProperty([0x00, 0x51], 2, "eq_att")
  EQ_ATT = ChannelProperty([0x00, 0x51], 2, "eq_att")
  EQ_ATT = ChannelProperty([0x00, 0x51], 2, "eq_att")


  pass

class ChannelMessage(SysExcMessage):

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
  
  def from_bytes(bytes: List[int]) -> SysExcMessage:
    print("### from bytes Not Implemented (SysExc message)")

  def update_desk(self, desk: Desk):
    print("### update desk Not Implemented (SysExc message)")

  def update_message(self) -> SysExcMessage | None:
    return SysExcMessage(self.address, [0, 0, 0, 0], self.size, self.messageType, MessageDirection.REQUEST_HOST)

  def request_update_messages(desk: Desk) -> List[DeskMessage]:
    print("### request_update_messages Not Implemented (SysExc message)")
    return []

  def check_bytes(bytes: List[int]) -> bool:
    if bytes[0] != 0xF0:
      return False
    if bytes[1] != 0x41:
      return False
    if bytes[2] != deviceId:
      return False
    if bytes[3:5] != modelId:
      return False
    if bytes[6] != 0x12:
      return False
    # bytes[7:10] == address
    # bytes[11:14] == data
    if bytes[-2] != calculate_checksum(bytes[7:-3]):
      return False
    if bytes[-1] != 0xF7:
      return False
    return True
  
  def check_server_type(type: str) -> bool:
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