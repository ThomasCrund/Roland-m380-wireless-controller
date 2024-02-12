from __future__ import annotations
from message import DeskMessage, MessageDirection, MessageType
from message.sysexc_message import SysExcMessage
from desk.input import InputSource, InputId, Input
from desk.desk import Desk
from typing import List, Callable
from enum import Enum

class InputBoardProperty():
  def __init__(self, address: List[int], size: int, name: str, data_range: tuple[int, int] = (0, 127), for_console = True):
    self.address = address
    self.size = size
    self.name = name
    self.data_range = data_range
    self.for_console = for_console

class InputBoardMessage(SysExcMessage):

  def __init__(self, inputBoardProperty: InputBoardProperty, data: List[int], id: InputId, direction: MessageDirection = MessageDirection.SET_TO_HOST, addressOffset: int = 0):
    if id.source == InputSource.CONSOLE and not inputBoardProperty.for_console:
      raise ValueError(f"InputBoard {inputBoardProperty.name} Message Used for not a console input")
    
    addressChannelNumber = 0
    if id.source == InputSource.CONSOLE: addressChannelNumber = 0x50 + id.number - 1
    if id.source == InputSource.REACT_A: addressChannelNumber = 0x00 + id.number - 1
    if id.source == InputSource.REACT_B: addressChannelNumber = 0x28 + id.number - 1

    address = [ 0x00, addressChannelNumber, inputBoardProperty.address[0], inputBoardProperty.address[1]]
    size = [ 0, 0, 0, inputBoardProperty.size]

    super().__init__(address, data, size, messageType=MessageType.CHANNEL, direction=direction)

    self.inputBoardProperty = inputBoardProperty
    self._id = id
    self.data = data
    self.addressOffset = addressOffset

  def from_bytes(self, bytes: List[int]) -> InputBoardMessage:
    address = bytes[7:11]
    data = bytes[11:-2]

    newId: InputId = None
    if address[1] < 0x28: newId = InputId(InputSource.REACT_A, address[1] - 0x00 + 1)
    elif address[1] < 0x50: newId = InputId(InputSource.REACT_B, address[1] - 0x28 + 1)
    else: newId = InputId(InputSource.REACT_A, address[1] - 0x50 + 1)

    return InputBoardMessage(self.inputBoardProperty, data, newId, MessageDirection.GET_FROM_HOST, address[3] - self.inputBoardProperty.address[1])

  def update_desk(self, desk: Desk, signalUpdate = True):
    input = desk.get_input(self._id)
    if self.inputBoardProperty.size == 1:
      input._properties[self.inputBoardProperty.check_server_type] = self.data[0]
    else:
      if len(self.data) == self.inputBoardProperty.size:
        input._properties[self.inputBoardProperty.check_server_type] = self.data
      else:
        if not self.inputBoardProperty.check_server_type in input._properties:
          input._properties[self.inputBoardProperty.check_server_type] = [0] * self.inputBoardProperty.size
        input._properties[self.inputBoardProperty.check_server_type][self.addressOffset] = self.data[0]
    if signalUpdate:
      desk.inputsChange = True
  
  def handle_client_message(self, id: InputId, data: List[int]):
    if not isinstance(data, List):
      data = [data]
    return InputBoardMessage(self.inputBoardProperty, data, id)

  def request_update_messages(self, desk: Desk) -> List[DeskMessage]:
    messages: List[InputBoardMessage] = []
    for input in desk.inputs:
      if (input._id.group == InputSource.CONSOLE):
        if self.inputBoardProperty.for_console:
          messages.append(InputBoardMessage(self.inputBoardProperty, self.data, input._id, MessageDirection.REQUEST_HOST))
      else:
        messages.append(InputBoardMessage(self.inputBoardProperty, self.data, input._id, MessageDirection.REQUEST_HOST))
    return messages

  def check_bytes(self, bytes: List[int]) -> bool:
    if not super().check_bytes(bytes):
      return False
    address = bytes[7:11]
    if not (address[0] == 0x03):
      return False
    if not (address[1] <= 0x2F):
      return False
    if not (address[2] == self.inputBoardProperty.address[0]):
      return False
    if (address[3] < self.inputBoardProperty.address[1] or (address[3]) >= (self.inputBoardProperty.address[1] + self.inputBoardProperty.size)):
      return False
    return True
  
  def get_all_interpreters() -> InputBoardMessage:
    id = InputId(InputSource.REACT_A, 1)
    messages = [
      InputBoardMessage(InputBoardProperty([0x00, 0x01], 1, "gain", (0, 37)), [], id, MessageDirection.INTERPRETER),
      InputBoardMessage(InputBoardProperty([0x00, 0x02], 1, "pad", (0, 1)), [], id, MessageDirection.INTERPRETER),
      InputBoardMessage(InputBoardProperty([0x00, 0x03], 1, "phantom", (0, 1)), [], id, MessageDirection.INTERPRETER),
      InputBoardMessage(InputBoardProperty([0x00, 0x04], 1, "link", (0, 1), False), [], id, MessageDirection.INTERPRETER),
    ]

    return messages
