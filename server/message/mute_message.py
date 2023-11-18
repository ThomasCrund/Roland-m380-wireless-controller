from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from desk.channel import ChannelId, Group, Channel
from desk import Desk
from typing import List

class MuteMessage(DeskMessage):
  def __init__(self, channelId: ChannelId, mute, direction: MessageDirection = MessageDirection.SET_TO_HOST):
    super().__init__(direction, MessageType.CHANNEL)
    self.channelId: ChannelId = channelId
    self.data = 0x01 if mute else 0x00

  def bytes(self):
    bytes = []
    bytes.append(0xB0 + self.channelId.get_MIDI_channel())
    bytes.append(self.channelId.get_MIDI_controller() + 63)
    bytes.append(self.data)
    return bytes
  
  def from_bytes(bytes: List[int]) -> MuteMessage:
    print("Reading", bytes)
    channelId: ChannelId = ChannelId.from_control_message_bytes(bytes[0:2], True)
    value = bytes[2]
    return MuteMessage(channelId, value, MessageDirection.GET_FROM_HOST)
  
  def update_desk(self, desk: Desk):
    channel = desk.get_channel(self.channelId)
    channel.mute = (self.data == 0x01)
    print(self.data, channel.mute)
    desk.channelChange = True
