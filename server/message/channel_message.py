from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from message.sysexc_message import SysExcMessage
from desk.channel import Group, ChannelId, Channel
from desk.desk import Desk
from typing import List, Callable
from enum import Enum

class ChannelProperty():
  def __init__(self, address: List[int], size: int, check_server_type: str, data_range: (int, int) = (0, 127), groups: List[Group] = [Group.FADER]):
    self.address = address
    self.size = size
    self.check_server_type = check_server_type
    self.data_range = data_range
    self.groups_supported = groups

class ChannelMessage(SysExcMessage):

  def __init__(self, channelProperty: ChannelProperty, data: List[int], channelId: ChannelId, direction: MessageDirection = MessageDirection.SET_TO_HOST, addressOffset: int = 0):
    addressNumber = 0
    if channelId.group == Group.FADER:
      addressNumber = 0x03
    elif channelId.group == Group.AUX:
      addressNumber = 0x05
    elif channelId.group == Group.MAIN:
      addressNumber = 0x06
    else:  
      raise ValueError("Channel Message Used for not a fader or Aux or Main, instead: ", channelId.group)
    
    address = [ addressNumber, (channelId.deskChannel - 1), channelProperty.address[0], channelProperty.address[1]]
    size = [ 0, 0, 0, channelProperty.size]

    super().__init__(address, data, size, messageType=MessageType.CHANNEL, direction=direction)

    self.channelProperty = channelProperty
    self.channelId = channelId
    self.data = data
    self.addressOffset = addressOffset

  def from_bytes(self, bytes: List[int]) -> ChannelMessage:
    address = bytes[7:11]
    data = bytes[11:-2]

    group = None
    if   address[0] == 0x03: group = Group.FADER
    elif address[0] == 0x05: group = Group.AUX
    elif address[0] == 0x06: group = Group.MAIN

    return ChannelMessage(self.channelProperty, data, ChannelId(group, address[1] + 1), MessageDirection.GET_FROM_HOST, address[3] - self.channelProperty.address[1])

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
      desk.channelsChangeUser = self.user
  
  def handle_client_message(self, channelId: ChannelId, data: List[int]):
    if not isinstance(data, List):
      data = [data]
    return ChannelMessage(self.channelProperty, data, channelId)

  def request_update_messages(self, desk: Desk) -> List[DeskMessage]:
    messages: List[ChannelMessage] = []
    for channel in desk.channels:
      if channel._id.group in self.channelProperty.groups_supported:
      # if (channel._id.group == Group.FADER) and channel._id.deskChannel == 5:
        messages.append(ChannelMessage(self.channelProperty, self.data, channel._id, MessageDirection.REQUEST_HOST))
    return messages

  def check_bytes(self, bytes: List[int]) -> bool:
    if not super().check_bytes(bytes):
      return False
    address = bytes[7:11]
    if not ((address[0] == 0x03 and Group.FADER in self.channelProperty.groups_supported)
            or (address[0] == 0x05 and Group.AUX in self.channelProperty.groups_supported)
            or (address[0] == 0x06 and Group.MAIN in self.channelProperty.groups_supported)):
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
    FAM = [Group.FADER, Group.AUX, Group.MAIN]
    FM = [Group.FADER, Group.MAIN]
    FA = [Group.FADER, Group.AUX]
    AM = [Group.AUX, Group.MAIN]
    messages = [
      ChannelMessage(ChannelProperty([0x00, 0x00], 6, "name", groups=FAM), [65] * 6, channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x06], 1, "name_color", (0, 7), groups=FAM), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x08], 1, "link", (0, 1), groups=FA), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x09], 1, "phase", (0, 1)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0A], 2, "att", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0C], 1, "mute", (0, 1), groups=FAM), [1], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0D], 1, "solo", (0, 1), groups=FAM), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0E], 2, "fader", groups=FAM), [64, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x10], 1, "pan", (1, 0x7F), groups=FAM), [65], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x11], 1, "main_switch", (0, 1)), [1], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x20], 1, "filter_switch", (0, 1)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x21], 1, "filter_type", (0, 3)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x22], 2, "filter_att", (0, 0x7F)), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x24], 3, "filter_freq", (0, 0x7f)), [0, 0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x27], 2, "filter_q", (0, 0x7f)), [0, 0], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x30], 1, "gate_switch", (0, 1)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x31], 1, "gate_key_in"), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x32], 1, "gate_mode", (0, 2)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x33], 2, "gate_threshold"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x35], 1, "gate_ratio", (0, 0x0d)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x36], 1, "gate_knee", (0, 9)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x37], 2, "gate_range"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x39], 2, "gate_attack"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x3B], 2, "gate_release"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x3D], 2, "gate_hold"), [0, 0], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x40], 1, "comp_switch", (0, 1)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x41], 1, "comp_key_in"), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x42], 2, "comp_threshold"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x44], 1, "comp_ratio", (0, 0x0d)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x45], 1, "comp_knee", (0, 9)), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x46], 2, "comp_attack"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x48], 2, "comp_release"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x4A], 2, "comp_hold"), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x4C], 1, "comp_switch", (0, 1)), [0], channelId, MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x50], 1, "eq_switch", (0, 1), groups=FAM), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x51], 2, "eq_att", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x53], 2, "eq_lo_gain", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x55], 3, "eq_lo_freq", groups=FAM), [0, 0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x58], 2, "eq_lo_mid_gain", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5A], 3, "eq_lo_mid_freq", groups=FAM), [0, 0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5D], 2, "eq_lo_mid_q", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5F], 2, "eq_hi_mid_gain", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x61], 3, "eq_hi_mid_freq", groups=FAM), [0, 0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x64], 2, "eq_hi_mid_q", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x66], 2, "eq_hi_gain", groups=FAM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x68], 3, "eq_hi_freq", groups=FAM), [0, 0, 0], channelId, MessageDirection.INTERPRETER),
      
      ChannelMessage(ChannelProperty([0x00, 0x70], 1, "limiter_switch", (0, 1), groups=AM), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x71], 2, "limiter_threshold", groups=AM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x73], 1, "limiter_knee", (0, 9), groups=AM), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x74], 2, "limiter_attack", groups=AM), [0, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x76], 2, "limiter_release", groups=AM), [0, 0], channelId, MessageDirection.INTERPRETER),
      
    ]

    for aux_num in range(1, 16):
      start_address = 8 * (aux_num - 1)
      messages += [
        ChannelMessage(ChannelProperty([0x01, start_address + 0], 1, f'aux{aux_num}_switch', (0, 1), groups=FM), [0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 1], 1, f'aux{aux_num}_position', (0, 2), groups=FM), [0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 2], 2, f'aux{aux_num}_level', groups=FM), [64, 0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 4], 1, f'aux{aux_num}_pan', (1, 0x7F), groups=FM), [0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 5], 1, f'aux{aux_num}_pan_link', (0, 1), groups=FM), [0], channelId, MessageDirection.INTERPRETER),
      ]

    messages += [
      ChannelMessage(ChannelProperty([0x02, 0x00], 1, f'main_switch', (0, 1), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x02, 0x01], 1, f'main_position', (0, 2), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x02, 0x02], 2, f'main_level', groups=[Group.AUX]), [64, 0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x02, 0x04], 1, f'main_pan', (1, 0x7F), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
    ]

    for mux_num in range(1, 8):
      start_address = 0x20 + 8 * (mux_num - 1)
      messages += [
        ChannelMessage(ChannelProperty([0x02, start_address + 0], 1, f'mux{aux_num}_switch', (0, 1), groups=AM), [0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x02, start_address + 1], 1, f'mux{aux_num}_position', (0, 2), groups=AM), [0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x02, start_address + 2], 2, f'mux{aux_num}_level', groups=AM), [64, 0], channelId, MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x02, start_address + 4], 1, f'mux{aux_num}_pan', (1, 0x7F), groups=AM), [0], channelId, MessageDirection.INTERPRETER),
      ]
    
    messages += [
      ChannelMessage(ChannelProperty([0x02, 0x70], 1, f'LCR_switch', (0, 1), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x02, 0x71], 1, f'LCR_centre', (0, 2), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x02, 0x72], 1, f'LR_switch', (0, 1), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x02, 0x73], 1, f'C_switch', (0, 1), groups=[Group.AUX]), [0], channelId, MessageDirection.INTERPRETER),
    ]

    return messages
