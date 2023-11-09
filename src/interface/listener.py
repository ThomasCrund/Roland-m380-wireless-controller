import mido
import threading
import time
from typing import List

from message import DeskMessage
import message
from desk import DeskController

class Listener(threading.Thread):
  def __init__(self, deskController: DeskController, inputPortName: str = None) -> None:
    threading.Thread.__init__(self)
    self.inputPortName = inputPortName
    self.setDaemon(True)
    self.last_message_time = None
    self.deskController: DeskController = deskController

  def run(self):
    self.port = mido.open_input(self.inputPortName, virtual = True)
    while (True):
      msg = self.port.receive(False)
      self.handle_message(msg)

      time.sleep(0.001)
    print(e)
    

  def handle_message(self, msg: mido.Message):
    print(msg.bytes())
    bytes = msg.bytes()
    messageInterpreted = None
    if (bytes[0] | 0xF0) == 0xB0:
      print('fader_signal')
      messageInterpreted = message.FaderMessage.from_bytes(msg.bytes())
    
    self.deskController.add_message(messageInterpreted)