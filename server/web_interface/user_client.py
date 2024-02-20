from enum import Enum

class ConnectionStatus(Enum):
  CONNECTED = 1
  DISCONNECTED = 2

class User:

  def __init__(self, sid, level) -> None:
    self.sid = sid
    self.status = ConnectionStatus.CONNECTED
    self.level = level

  def setConnectionStatus(self, status: ConnectionStatus):
    self.status = status

  