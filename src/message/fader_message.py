from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from desk.channel import ChannelId, Group, Channel
from desk import Desk
from typing import List

class FaderMessage(DeskMessage):
  def __init__(self, channelId: ChannelId, data, direction: MessageDirection = MessageDirection.SET_TO_HOST):
    super().__init__(direction, MessageType.CHANNEL)
    self.channelId: ChannelId = channelId
    self.data = data

  def bytes(self):
    bytes = []
    bytes.append(0xB0 + self.channelId.get_MIDI_channel())
    bytes.append(self.channelId.get_MIDI_controller())
    bytes.append(self.data)
    return bytes
  
  def from_bytes(bytes: List[int]) -> FaderMessage:
    channelId: ChannelId = ChannelId.from_control_message_bytes(bytes[0:1])
    value = bytes[2]
    return FaderMessage(channelId, value, MessageDirection.GET_FROM_HOST)
  
  def update_desk(self, desk: Desk):
    channel = desk.get_channel(self.channelId)
    channel.fader = self.data
