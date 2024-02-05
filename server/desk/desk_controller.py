from desk.desk import Desk
from desk.desk_connection import DeskConnection
from desk.channel import channels_to_JSON, Group, ChannelId
from typing import List
from message import DeskMessage, FaderMessage, MuteMessage
from message.message_controller import MessageController
from message.channel_message import ChannelMessage
from web_interface import Server

class DeskController:

  def __init__(self, desk: Desk, deskConnection: DeskConnection):
    self.desk = desk
    self.incomingMessages: List[DeskMessage] = []
    self._listener_connected = False
    self.deskConnection = deskConnection
    self.messageController = MessageController()
    self.messageController.add_interpreters(ChannelMessage.get_all_interpreters())
    self.desk.initialise_channels()

    self.last_connection = None

  def run(self, server: Server):
    server.send_channels(channels_to_JSON(self.desk.channels))

    messages = self.messageController.request_update_messages(self.desk)
    self.deskConnection._message_to_host += messages

    while True:

      # handle incoming messages from desk
      while len(self.deskConnection.messages_from_host) != 0:
        message: DeskMessage = self.deskConnection.messages_from_host.pop(0)
        message.update_desk(self.desk)

      print(self.desk.channels[4]._properties)

      # Get requests from the client and send to the desk
      self.check_client_requests(server)

      # update desk connection and desk outgoing messages
      self.deskConnection.update()

      # Update clients on desk settings and connection status
      self.update_server(server)

      server.socketio.sleep(0.01)

  def add_message(self, message: DeskMessage):
    self.incomingMessages.append(message)

  def check_client_requests(self, server: Server):
    while len(server.client_requests) != 0:
      request = server.client_requests.pop(0)
      print(request)
      if request['type'] == 'channel-fader-set':
        message = FaderMessage(ChannelId(Group(request['group']), request['channelNum']), request['value'])
        print(message.hex())
        self.deskConnection.add_message_to_host(message)
      elif request['type'] == 'channel-mute-set':
        message = MuteMessage(ChannelId(Group(request['group']), request['channelNum']), request['value'])
        print(message.hex())

  def update_server(self, server: Server):

    # Check desk
    if self.desk.channelChange:
      server.send_channels(channels_to_JSON(self.desk.channels))
      self.desk.channelChange = False
    
    # Check connection
    if (self.deskConnection.connected != self.last_connection) or self.last_connection == None:
      server.send_desk_connected(self.deskConnection.connected)
      self.last_connection = self.deskConnection.connected
      

    