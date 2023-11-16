from enum import Enum
from desk.channel import Channel, ChannelId, Group
from typing import List

class Desk:
  def __init__(self) -> None:
    self.channels: List[Channel] = []
    self.channelChange = False
    self.patchbayChange = False

  def get_channel(self, channelId: ChannelId):

    # Find channel if existing
    for channel in self.channels:
      if channel.id == channelId:
        return channel

    # Create Channel if not yet known
    newChannel = Channel(channelId)
    self.channels.append(newChannel)
    return newChannel
  
  def initialise_group(self, group: Group, startId: int, endId: int):
    for i in range(startId, endId + 1):
      self.channels.append(Channel(ChannelId(group, i)))

  def initialise_channels(self):
    self.initialise_group(Group.FADER, 1, 48)