import mido
import threading
import src.message as message

from desk import Desk

class Listener(threading.Thread):
  def __init__(self, desk: Desk, input: str = None) -> None:
    self.input = input
    self.desk = desk
    self.setDaemon(True)
    self.messages

  def run(self):
    with mido.open_input() as input:
      for msg in input:
        self.handle_message(msg)

  def handle_message(self, msg: mido.Message):
    print(msg.bytes())
    bytes = msg.bytes()
    messageInterpreted = None
    if (bytes[0] | 0xF0) == 0xB0:
      print('fader_signal')
      messageInterpreted = message.FaderMessage.from_bytes(msg.bytes())