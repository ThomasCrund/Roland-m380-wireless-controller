import mido

class DeskMessage:
  def __init__(self, bytes):
    self.bytes = bytes

  def get_value(self):
    pass

  def get_data(self):
    pass

  def get_msg(self):
    return mido.Message.from_bytes(bytes)
  
  def bytes(self):
    return bytes

  def hex(self):
    output = ""
    for byte in bytes:
      output += hex(byte) + " "
    return output

  def construct_fader_message():







