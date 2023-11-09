from __future__ import annotations
from message import DeskMessage
from desk.channel import ChannelId, Group
from types import List

class FaderMessage(DeskMessage):
  def __init__(self, channelId: ChannelId, value):
    super(self.generate_bytes(channelId, value))
    self.channelId: ChannelId = channelId,
    self.value = value

  def generate_bytes(channelId: ChannelId, value: int):
    bytes = []
    bytes.append(0xB0 + channelId.get_MIDI_channel())
    bytes.append(0xB0 + channelId.get_MIDI_channel())
    bytes.append(value)
    return bytes
  
  def from_bytes(bytes: List[int]) -> FaderMessage:
    channelId: ChannelId = ChannelId.from_control_message_bytes(bytes[0:1])
    value = bytes[2]
    return FaderMessage(channelId, value)
  
