from enum import Enum
from src.desk.channel import Channel, ChannelId, Group
from src.message import DeskMessage

class Desk:
  def __init__(self) -> None:
    self.channels: Channel = []

  def handle_message(message: DeskMessage):
    print('handling')

  
  