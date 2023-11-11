from enum import Enum
from desk.channel import Channel, ChannelId, Group
from typing import List

class Desk:
  def __init__(self) -> None:
    self.channels: List[Channel] = []

  def get_channel(self, channelId: ChannelId):

    # Find channel if existing
    for channel in self.channels:
      if channel.id == channelId:
        return channel

    # Create Channel if not yet known
    newChannel = Channel(channelId)
    self.channels.append(newChannel)
    return newChannel