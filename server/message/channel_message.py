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


class ChannelMessage(SysExcMessage):

  def __init__(self, channelProperty: ChannelProperty, data: List[int], direction: MessageDirection = MessageDirection.SET_TO_HOST):
    address = []
    size = []

    super().__init__(address, data, size, messageType=MessageType.CHANNEL, direction=direction)

    self.channelProperty = channelProperty

  
  def from_bytes(bytes: List[int]) -> SysExcMessage:
    print("### from bytes Not Implemented (SysExc message)")

  def update_desk(self, desk: Desk):
    print("### update desk Not Implemented (SysExc message)")

  def request_update_messages(desk: Desk) -> List[DeskMessage]:
    print("### request_update_messages Not Implemented (SysExc message)")
    return []

  def check_bytes(bytes: List[int]) -> bool:
    if not super().check_bytes(bytes):
      return False
  
  def get_all_interpreters() -> ChannelMessage:
    messages = [
      ChannelMessage(ChannelProperty([0x00, 0x00], 6, "name"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x06], 1, "name_color", (0, 7)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x08], 1, "link", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x09], 1, "phase", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0A], 2, "att"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0C], 1, "mute", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0D], 1, "solo", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x0E], 2, "fader"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x10], 1, "pan", (1, 0x7F)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x11], 1, "main_switch", (0, 1)), [], MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x20], 1, "filter_switch", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x21], 1, "filter_type", (0, 3)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x22], 2, "filter_att", (0, 0x7F)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x24], 3, "filter_freq", (0, 0x7f)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x27], 2, "filter_q", (0, 0x7f)), [], MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x30], 1, "gate_switch", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x31], 1, "gate_key_in"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x32], 1, "gate_mode", (0, 2)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x33], 2, "gate_threshold"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x35], 1, "gate_ratio", (0, 0x0d)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x36], 1, "gate_knee", (0, 9)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x37], 2, "gate_range"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x39], 2, "gate_attack"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x3B], 2, "gate_release"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x3D], 2, "gate_hold"), [], MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x40], 1, "comp_switch", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x41], 1, "comp_key_in"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x42], 2, "comp_threshold"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x44], 1, "comp_ratio", (0, 0x0d)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x45], 1, "comp_knee", (0, 9)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x46], 2, "comp_attack"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x48], 2, "comp_release"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x4A], 2, "comp_hold"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x4C], 1, "comp_switch", (0, 1)), [], MessageDirection.INTERPRETER),

      ChannelMessage(ChannelProperty([0x00, 0x50], 1, "eq_switch", (0, 1)), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x51], 2, "eq_att"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x53], 2, "lo_gain"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x55], 3, "lo_freq"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x58], 2, "lo_mid_gain"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5A], 3, "lo_mid_freq"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5D], 2, "lo_mid_q"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x5F], 2, "hi_mid_gain"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x61], 3, "hi_mid_freq"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x64], 2, "hi_mid_q"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x66], 2, "hi_gain"), [], MessageDirection.INTERPRETER),
      ChannelMessage(ChannelProperty([0x00, 0x68], 3, "hi_freq"), [], MessageDirection.INTERPRETER),
    ]

    for aux_num in range(1, 16):
      start_address = 8 * (aux_num - 1)
      messages += [
        ChannelMessage(ChannelProperty([0x01, start_address + 0], 1, f'aux{aux_num}_switch', (0, 1)), [], MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 1], 1, f'aux{aux_num}_position', (0, 2)), [], MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 2], 2, f'aux{aux_num}_level'), [], MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 4], 1, f'aux{aux_num}_pan', (1, 0x7F)), [], MessageDirection.INTERPRETER),
        ChannelMessage(ChannelProperty([0x01, start_address + 5], 1, f'aux{aux_num}_pan_link', (0, 1)), [], MessageDirection.INTERPRETER),
      ]

    return messages
