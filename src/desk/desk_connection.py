import mido
import threading
import time
from typing import List
import rtmidi._rtmidi as rtmidi

from message import DeskMessage, FaderMessage
from desk.channel import Group, ChannelId
import message

class DeskConnection():
  def __init__(self, inputPortName: str = None, outputPortName: str = None) -> None:
    self.inputPortName = inputPortName
    self.outputPortName = outputPortName

    self.input_port = None
    self.output_port = None

    self._message_from_host: List[DeskMessage] = []
    self._message_to_host: List[DeskMessage] = []

    self.last_message_time = None
    self._connected = False
    
  def connect_to_desk(self) -> bool:
    connected = True

    if self.input_port == None:
      try:
        self.input_port = mido.open_input(self.inputPortName, callback=self.message_callback)
        print("Input Connected")
      except IOError as err:
        if (str(err) == "no ports available"):
          print("Input Not Connected")
          self.input_port = None
          connected = False
        else:
          print("Input connection error: ", err)
          connected = False
  
    if self.output_port == None:
      try:
        self.output_port = mido.open_output(self.outputPortName)
        print("Output Connected")
      except IOError as err:
        if (str(err) == f"unknown port '{self.outputPortName}'"):
          print("Output Not Connected")
          self.output_port = None
          connected = False
        else:
          print("Output connection error: ", err)
          connected = False

    self._connected = connected
    return self.connected

  def send_output_message(self):
    for message in self._message_to_host:
      try:
        self.output_port.send(message.get_msg())
        self._message_to_host.remove(message)
      except rtmidi.SystemError as err:
        print("Error: ", err)
        self._connected = False
        self.input_port = None
        self.output_port = None
        return


  

  def update(self):
    if not self.connect_to_desk():
      return
    
    print(self.input_port, self.output_port)
    channel = ChannelId(Group.FADER, 5)
    print("Channel", channel)
    message = FaderMessage(channel, 100)
    self._message_to_host.append(message)
    

    self.send_output_message()

  
    
  @property
  def connected(self):
    return self._connected

  @connected.setter
  def set_connected(self, connected: bool):
    self._listener_connected = True
    self._connected = self._listener_connected

  @property
  def message_from_host(self):
    return self._connected

  @property
  def message_to_host(self):
    return self._connected

  def message_callback(self, msg: mido.Message):
    print(msg.bytes())
    bytes = msg.bytes()
    messageInterpreted = None
    if (bytes[0] | 0xF0) == 0xB0:
      print('fader_signal')
      messageInterpreted = message.FaderMessage.from_bytes(msg.bytes())
    