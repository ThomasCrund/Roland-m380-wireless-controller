import mido
import threading
import time
from typing import List
import rtmidi._rtmidi as rtmidi

from message import DeskMessage, MessageController
from desk.channel import Group, ChannelId
import message

class DeskConnection():
  def __init__(self, inputPortName: str = None, outputPortName: str = None) -> None:
    self.inputPortName = inputPortName
    self.outputPortName = outputPortName

    self.input_port = None
    self.output_port = None

    self.mc = MessageController()

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

  def send_output_messages(self):
    for message in self._message_to_host:
      try:
        print("### Sending message", message.hex())
        print(message.hex())
        self.output_port.send(message.get_msg())
        self._message_to_host.remove(message)
      except rtmidi.SystemError as err:
        print("Error: ", err)
        self.close_ports()
        return

  def close_ports(self):
    self._connected = False
    self.input_port.close()
    self.output_port.close()
    self.input_port = None
    self.output_port = None
  

  def update(self):
    if not self.connect_to_desk():
      return
    
    # print(self.input_port, self.output_port)
    # channel = ChannelId(Group.FADER, 5)
    # print("Channel", channel)
    # message = FaderMessage(channel, 100)
    # self._message_to_host.append(message)
    

    self.send_output_messages()
    
  @property
  def connected(self):
    return self._connected

  @property
  def messages_from_host(self):
    return self._message_from_host

  @property
  def messages_to_host(self):
    return self._message_to_host
  
  def add_message_to_host(self, message):
    self._message_to_host.append(message)

  def message_callback(self, msg: mido.Message):
    try:
      bytes = msg.bytes()
      messageInterpreted = self.mc.interpret_message_from_bytes(bytes)
      self._message_from_host.append(messageInterpreted)
    except Exception as e:
      print('error', e)