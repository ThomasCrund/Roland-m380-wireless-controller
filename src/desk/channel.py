from __future__ import annotations
from enum import Enum
from typing import List

class Group(Enum):
  FADER = 1
  DCA = 2
  MTX = 3
  AUX = 4
  MAIN = 5

class ChannelId:
  def __init__(self, group: Group, deskChannel: int):
    self.group = group
    self.deskChannel = deskChannel

  def get_MIDI_channel(self):
    if self.group == Group.FADER:
      if self.deskChannel <= 24:
        return 0x0
      else:
        return 0x1
    elif self.group == Group.DCA:
      return 0x9
    elif self.group == Group.MTX:
      return 0xD
    elif self.group == Group.AUX:
      return 0xE
    elif self.group == Group.MAIN:
      return 0xF
    
  def get_MIDI_controller(self):
    if self.group == Group.FADER:
      if self.deskChannel <= 24:
        return self.deskChannel
      else:
        return self.deskChannel - 24
    elif self.group == Group.DCA:
      return self.deskChannel
    elif self.group == Group.MTX:
      return self.deskChannel
    elif self.group == Group.AUX:
      return self.deskChannel
    elif self.group == Group.MAIN:
      return self.deskChannel    
    
  def __eq__(self, __value: object) -> bool:
    return (self.deskChannel == __value.deskChannel) and (self.group == __value.group)
    
  def from_control_message_bytes(bytes: List[int]) -> ChannelId:
    group = 0xFF
    deskChannel = None
    maxController = 0
    minController = 1

    # group
    if bytes[0] == 0xB0: 
      group = Group.FADER
      maxController = 24
    elif bytes[0] == 0xB1: 
      group = Group.FADER
      minController = 25
      maxController = 48
    elif bytes[0] == 0xB9: 
      group = Group.DCA
      maxController = 8
    elif bytes[0] == 0xBD: 
      group = Group.MTX
      maxController = 8
    elif bytes[0] == 0xBE: 
      group = Group.AUX
      maxController = 8
    elif bytes[0] == 0xBF: 
      group = Group.MAIN
      maxController = 3
    else:
      raise ValueError(f"Channel Parse control message bytes: {bytes[0]} {bytes[1]}, channel input incorrect")

    if bytes[1] < minController or bytes[1] > maxController:
      raise ValueError(f"Channel Parse control message bytes: {bytes[0]} {bytes[1]}, controller out of range")

    # deskChannel
    if bytes[0] == 0xB1: deskChannel = bytes[1] + 24
    else: deskChannel = bytes[1]
    
    return ChannelId(group, deskChannel)


class Channel:
  def __init__(self, id: ChannelId):
    self._id = id
    self._fader = None
    self._mute = None

  def setFader(self, value):
    self._fader = value
  
  def setMute(self, value):
    self._mute = value

  def __eq__(self, __value: object) -> bool:
    return self.id == __value.id