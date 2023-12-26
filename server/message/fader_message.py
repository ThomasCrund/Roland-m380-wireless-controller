from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from desk.channel import ChannelId, Group, Channel
from desk.desk import Desk
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
    channelId: ChannelId = ChannelId.from_control_message_bytes(bytes[0:2])
    value = bytes[2]
    return FaderMessage(channelId, value, MessageDirection.GET_FROM_HOST)
  
  def update_desk(self, desk: Desk):
    channel = desk.get_channel(self.channelId)
    channel.fader = self.data
    desk.channelChange = True

  def update_message(channelId: ChannelId) -> DeskMessage | None:
    return None

  def request_update_messages(desk: Desk) -> List[DeskMessage]:
    messages: List[DeskMessage] = []
    for channel in desk.channels:
      message = FaderMessage.update_message()
      if (message != None):
        messages.append(message)
    return messages

  def check_bytes(bytes: List[int]) -> bool:
    return (bytes[0] & 0xF0) == 0xB0 and bytes[1] < 0x40
  
  def check_server_type(type: str) -> bool:
    return type == "fader"
    
