from desk.desk import Desk
from desk.desk_connection import DeskConnection
from desk.channel import channels_to_JSON
from typing import List
from message import DeskMessage
from web_interface import Server

class DeskController:

  def __init__(self, desk: Desk, deskConnection: DeskConnection):
    self.desk = desk
    self.incomingMessages: List[DeskMessage] = []
    self._listener_connected = False
    self.desk.initialise_channels()
    self.deskConnection = deskConnection

    self.last_connection = None

  def run(self, server: Server):
    while True:

      # handle incoming messages from desk
      while len(self.deskConnection.messages_from_host) != 0:
        message: DeskMessage = self.deskConnection.messages_from_host.pop(0)
        message.update_desk(self.desk)

      # update desk connection and desk outgoing messages
      self.deskConnection.update()

      # Update clients on desk settings and connection status
      self.update_server(server)

      server.socketio.sleep(1)

  def add_message(self, message: DeskMessage):
    self.incomingMessages.append(message)

  def update_server(self, server: Server):

    # Check desk
    if self.desk.channelChange:
      server.send_channels(channels_to_JSON(self.desk.channels))
      self.desk.channelChange = False
    
    # Check connection
    if (self.deskConnection.connected != self.last_connection) or self.last_connection == None:
      server.send_desk_connected(self.deskConnection.connected)
      self.last_connection = self.deskConnection.connected
      

    