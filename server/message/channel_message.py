from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from message.sysexc_message import SysExcMessage
from desk.channel import Group, ChannelId, Channel
from desk.desk import Desk
from typing import List, Callable
from enum import Enum

class ChannelProperty():
  def __init__(self, address: List[int], size: int, check_server_type: str, data_range: (int, int) = (0, 127)):
    self.address = address
    self.size = size
    self.check_server_type = check_server_type
    self.data_range = data_range

class ChannelMessage(SysExcMessage):

  def __init__(self, channelProperty: ChannelProperty, data: List[int], channelId: ChannelId, direction: MessageDirection = MessageDirection.SET_TO_HOST, addressOffset: int = 0):
    if channelId.group != Group.FADER:
      raise ValueError("Channel Message Used for not a fader")
    
    address = [ 0x03, (channelId.deskChannel - 1), channelProperty.address[0], channelProperty.address[1]]
    size = [ 0, 0, 0, channelProperty.size]

    super().__init__(address, data, size, messageType=MessageType.CHANNEL, direction=direction)

    self.channelProperty = channelProperty
    self.channelId = channelId
    self.data = data
    self.addressOffset = addressOffset

  def from_bytes(self, bytes: List[int]) -> ChannelMessage:
    address = bytes[7:11]
    data = bytes[11:-2]
    return ChannelMessage(self.channelProperty, data, ChannelId(Group.FADER, address[1] + 1), MessageDirection.GET_FROM_HOST, address[3] - self.channelProperty.address[1])

  def update_desk(self, desk: Desk, signalUpdate = True):
    for channel in desk.channels:
      if (channel._id == self.channelId):
        if self.channelProperty.size == 1:
          channel._properties[self.channelProperty.check_server_type] = self.data[0]
        else:
          if len(self.data) == self.channelProperty.size:
            channel._properties[self.channelProperty.check_server_type] = self.data
          else:
            if not self.channelProperty.check_server_type in channel._properties:
              channel._properties[self.channelProperty.check_server_type] = [0] * self.channelProperty.size
            channel._properties[self.channelProperty.check_server_type][self.addressOffset] = self.data[0]
    if signalUpdate:
      desk.channelChange = True
  
  def handle_client_message(self, channelId: ChannelId, data: List[int]):
    if not isinstance(data, List):
      data = [data]
    return ChannelMessage(self.channelProperty, data, channelId)

  def request_update_messages(self, desk: Desk) -> List[DeskMessage]:
    messages: List[ChannelMessage] = []
    for channel in desk.channels:
      if (channel._id.group == Group.FADER):
      # if (channel._id.group == Group.FADER) and channel._id.deskChannel == 5:
        messages.append(ChannelMessage(self.channelProperty, self.data, channel._id, MessageDirection.REQUEST_HOST))
    return messages

  def check_bytes(self, bytes: List[int]) -> bool:
    if not super().check_bytes(bytes):
      return False
    address = bytes[7:11]
    if not (address[0] == 0x03):
      return False
    if not (address[1] <= 0x2F):
      return False
    if not (address[2] == self.channelProperty.address[0]):
      return False
    if (address[3] < self.channelProperty.address[1] or (address[3]) >= (self.channelProperty.address[1] + self.channelProperty.size)):
      return False
    return True
  
  def get_all_interpreters() -> ChannelMessage:
    channelId = ChannelId(Group.FADER, 0)
    messages = [
      ChannelMessage(ChannelProperty([0x00, 0x00], 6, "name"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x06], 1, "name_color", (0, 7)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x08], 1, "link", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x09], 1, "phase", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0A], 2, "att"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0C], 1, "mute", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0D], 1, "solo", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0E], 2, "fader"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x10], 1, "pan", (1, 0x7F)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x11], 1, "main_switch", (0, 1)), [], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x20], 1, "filter_switch", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x21], 1, "filter_type", (0, 3)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x22], 2, "filter_att", (0, 0x7F)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x24], 3, "filter_freq", (0, 0x7f)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x27], 2, "filter_q", (0, 0x7f)), [], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x30], 1, "gate_switch", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x31], 1, "gate_key_in"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x32], 1, "gate_mode", (0, 2)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x33], 2, "gate_threshold"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x35], 1, "gate_ratio", (0, 0x0d)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x36], 1, "gate_knee", (0, 9)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x37], 2, "gate_range"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x39], 2, "gate_attack"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x3B], 2, "gate_release"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x3D], 2, "gate_hold"), [], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x40], 1, "comp_switch", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x41], 1, "comp_key_in"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x42], 2, "comp_threshold"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x44], 1, "comp_ratio", (0, 0x0d)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x45], 1, "comp_knee", (0, 9)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x46], 2, "comp_attack"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x48], 2, "comp_release"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x4A], 2, "comp_hold"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x4C], 1, "comp_switch", (0, 1)), [], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x50], 1, "eq_switch", (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x51], 2, "eq_att"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x53], 2, "lo_gain"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x55], 3, "lo_freq"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x58], 2, "lo_mid_gain"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5A], 3, "lo_mid_freq"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5D], 2, "lo_mid_q"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5F], 2, "hi_mid_gain"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x61], 3, "hi_mid_freq"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x64], 2, "hi_mid_q"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x66], 2, "hi_gain"), [], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x68], 3, "hi_freq"), [], channelId, MessageDirection.INTERPRETER),
    ]

    for aux_num in range(1, 16):
      start_address = 8 * (aux_num - 1)
      messages += [
        ChannelMessage(ChannelProperty([0x01, start_address + 0], 1, f'aux{aux_num}_switch', (0, 1)), [], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 1], 1, f'aux{aux_num}_position', (0, 2)), [], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 2], 2, f'aux{aux_num}_level'), [], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 4], 1, f'aux{aux_num}_pan', (1, 0x7F)), [], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 5], 1, f'aux{aux_num}_pan_link', (0, 1)), [], channelId, MessageDirection.INTERPRETER),
      ]

    return messages
