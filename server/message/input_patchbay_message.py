from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from message.sysexc_message import SysExcMessage
from desk.input import InputSource, InputId
from desk.channel import ChannelId, Group
from desk.desk import Desk
from typing import List

class InputPatchbayMessage(SysExcMessage):

  def __init__(self, inputId: InputId, channelId: ChannelId, direction: MessageDirection = MessageDirection.SET_TO_HOST, addressOffset: int = 0):
    if channelId.group != Group.FADER:
      raise ValueError("Channel Message Used for not a fader")
    
    addressChannelNumber = channelId.deskChannel - 1

    address = [ 0x02, addressChannelNumber, 0, 0]
    size = [ 0, 0, 0, 1]
    
    inputChannelId = 127
    if inputId.source == InputSource.REACT_A: inputChannelId = inputId.number + 0 - 1; 
    elif inputId.source == InputSource.REACT_B: inputChannelId = inputId.number + 40 - 1; 
    elif inputId.source == InputSource.CONSOLE: inputChannelId = inputId.number + 80 - 1; 
    elif inputId.source == InputSource.STEREO_IN: inputChannelId = inputId.number + 88 - 1; 
    elif inputId.source == InputSource.PLAY: inputChannelId = inputId.number + 92 - 1; 
    elif inputId.source == InputSource.FX1: inputChannelId = inputId.number + 94 - 1; 
    elif inputId.source == InputSource.FX2: inputChannelId = inputId.number + 96 - 1; 
    elif inputId.source == InputSource.FX3: inputChannelId = inputId.number + 98 - 1; 
    elif inputId.source == InputSource.FX4: inputChannelId = inputId.number + 100 - 1; 

    data = [inputChannelId]

    super().__init__(address, data, size, messageType=MessageType.CHANNEL, direction=direction)

    self._id = channelId
    self.data = data
    self.addressOffset = addressOffset
    self.inputId = inputId

  def from_bytes(self, bytes: List[int]) -> InputPatchbayMessage:
    address = bytes[7:11]
    data = bytes[11:-2]

    inputId: InputId = None
    if data[0] <= 39: inputId = InputId(InputSource.REACT_A, data[0] + 1)
    elif data[0] <= 79: inputId = InputId(InputSource.REACT_B, data[0] - 39)
    elif data[0] <= 87: inputId = InputId(InputSource.CONSOLE, data[0] - 79)
    elif data[0] <= 89: inputId = InputId(InputSource.STEREO_IN, data[0] - 87)
    elif data[0] <= 91: raise IndexError("Not a valid patchbay input address: ", data[0])
    elif data[0] <= 93: inputId = InputId(InputSource.PLAY, data[0] - 91)
    elif data[0] <= 95: inputId = InputId(InputSource.FX1, data[0] - 93)
    elif data[0] <= 97: inputId = InputId(InputSource.FX2, data[0] - 95)
    elif data[0] <= 99: inputId = InputId(InputSource.FX3, data[0] - 97)
    elif data[0] <= 101: inputId = InputId(InputSource.FX4, data[0] - 99)
    elif data[0] <= 126: raise IndexError("Not a valid patchbay input address: ", data[0])
    elif data[0] == 127: inputId = InputId(InputSource.NONE, 0)

    channelId = ChannelId(Group.FADER, address[1] + 1)

    return InputPatchbayMessage(inputId, channelId, MessageDirection.GET_FROM_HOST)

  def update_desk(self, desk: Desk, signalUpdate = True):
    channel = desk.get_channel(self._id)
    channel.inputId = self.inputId
    if signalUpdate:
      desk.channelChange = True
  
  def handle_client_message(self, id: ChannelId, data: InputId):
    
    return InputPatchbayMessage(data, id)

  def request_update_messages(self, desk: Desk) -> List[DeskMessage]:
    messages: List[InputPatchbayMessage] = []
    for channel in desk.channels:
      if (channel._id.group == Group.FADER):
        messages.append(InputPatchbayMessage(InputId(InputSource.REACT_A, 1), channel._id, MessageDirection.REQUEST_HOST))
    return messages

  def check_bytes(self, bytes: List[int]) -> bool:
    if not super().check_bytes(bytes):
      return False
    address = bytes[7:11]
    if not (address[0] == 0x02):
      return False
    if not (address[1] <= 0x2F):
      return False
    if not (address[2] == 0x00):
      return False
    if not (address[3] == 0x00):
      return False
    return True
  
  def get_all_interpreters() -> InputPatchbayMessage:
    messages = [
      InputPatchbayMessage(InputId(InputSource.REACT_A, 1), ChannelId(Group.FADER, 1), MessageDirection.INTERPRETER),
    ]

    return messages
