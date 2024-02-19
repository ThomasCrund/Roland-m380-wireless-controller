from enum import Enum
from desk.channel import Channel, ChannelId, Group
from desk.input import Input, InputId, InputSource
from typing import List

class Desk:
  def __init__(self) -> None:
    self.channels: List[Channel] = []
    self.inputs: List[Input] = []
    self.channelChange = False
    self.inputsChange = False

  def get_channel(self, channelId: ChannelId):

    # Find channel if existing
    for channel in self.channels:
      if channel._id == channelId:
        return channel

    # Create Channel if not yet known
    newChannel = Channel(channelId)
    self.channels.append(newChannel)
    return newChannel
  
  def get_input(self, inputId: InputId):

    # Find channel if existing
    for input in self.inputs:
      if input._id == inputId:
        return input

    # Create Channel if not yet known
    newInput = Input(inputId)
    self.inputs.append(newInput)
    return newInput
  
  def initialise_group(self, group: Group, startId: int, endId: int):
    for i in range(startId, endId + 1):
      channel = Channel(ChannelId(group, i))
      if group == Group.FADER:
        channel.set_property('fader', [64, 0])
        channel.set_property('mute', 1)
        channel.set_property('name', [65, 65, 65, 65, 65, 65])
        channel.set_property('name_color', i % 7)
      self.channels.append(channel)
    self.channelChange = True

  def initialise_channels(self):
    self.initialise_group(Group.FADER, 1, 48)

  def initialise_input_source(self, inputSource: InputSource, startId: int, endId: int):
    for i in range(startId, endId + 1):
      self.inputs.append(Input(InputId(inputSource, i)))

  def initialise_inputs(self):
    self.initialise_input_source(InputSource.CONSOLE, 1, 8)
    self.initialise_input_source(InputSource.REACT_A, 1, 40)
    self.initialise_input_source(InputSource.REACT_B, 1, 40)
    self.initialise_input_source(InputSource.FX1, 1, 2)
    self.initialise_input_source(InputSource.FX2, 1, 2)
    self.initialise_input_source(InputSource.FX3, 1, 2)
    self.initialise_input_source(InputSource.FX4, 1, 2)
    self.initialise_input_source(InputSource.STEREO_IN, 1, 2)
    self.initialise_input_source(InputSource.PLAY, 1, 2)
    self.initialise_input_source(InputSource.NONE, 0, 0)