from desk.desk import Desk
from desk.desk_connection import DeskConnection
from desk.channel import channels_to_JSON, Group, ChannelId
from desk.input import inputs_to_JSON, InputSource, InputId
from typing import List
from message import DeskMessage
from message.message_controller import MessageController
from message.channel_message import ChannelMessage
from message.input_board_message import InputBoardMessage
from message.input_patchbay_message import InputPatchbayMessage
from web_interface import Server

class DeskController:

  def __init__(self, desk: Desk, deskConnection: DeskConnection):
    self.desk = desk
    self.incomingMessages: List[DeskMessage] = []
    self._listener_connected = False
    self.deskConnection = deskConnection
    self.messageController = MessageController()
    self.messageController.add_interpreters(ChannelMessage.get_all_interpreters())
    self.messageController.add_interpreters(InputBoardMessage.get_all_interpreters())
    self.messageController.add_interpreters(InputPatchbayMessage.get_all_interpreters())
    self.desk.initialise_channels()
    self.desk.initialise_inputs()

    self.last_connection = None

  def run(self, server: Server):
    server.send_list('channels', channels_to_JSON(self.desk.channels))

    messages = self.messageController.request_update_messages(self.desk)
    self.set_default_values(messages)
    self.deskConnection._message_to_host += messages

    while True:

      # handle incoming messages from desk
      while len(self.deskConnection.messages_from_host) != 0:
        message: DeskMessage = self.deskConnection.messages_from_host.pop(0)
        message.update_desk(self.desk)

      # print(self.desk.inputs[3]._id.source, self.desk.inputs[3]._id.number, self.desk.inputs[3]._properties)
      num = 3
      # print(self.desk.channels[num]._id.group, self.desk.channels[num]._id.deskChannel, self.desk.channels[num].inputId)

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
      for messageInterpreter in self.messageController.messageInterpreters:
        if isinstance(messageInterpreter,  ChannelMessage):
          if request['type'] == "channel" and request['property'] == messageInterpreter.channelProperty.check_server_type:
            message = messageInterpreter.handle_client_message(ChannelId(Group(request['group']), request['channelNum']), request['value'])
            message.update_desk(self.desk, request['update_itself'])
            self.deskConnection.add_message_to_host(message)
            return
        if isinstance(messageInterpreter,  InputBoardMessage):
          if request['type'] == "input" and request['property'] == messageInterpreter.inputBoardProperty.name:
            message = messageInterpreter.handle_client_message(InputId(InputSource(request['inputSource']), request['inputNumber']), request['value'])
            message.update_desk(self.desk, True)
            self.deskConnection.add_message_to_host(message)
            return
        if isinstance(messageInterpreter,  InputPatchbayMessage):
          if request['type'] == "channel" and request['property'] == "input":
            print(request)
            message = messageInterpreter.handle_client_message(ChannelId(Group(request['group']), request['channelNum']), InputId(InputSource(request['value']['inputSource']), request['value']['inputNumber']))
            message.update_desk(self.desk, True)
            self.deskConnection.add_message_to_host(message)
            return
        
      print("Request not know", request)
      

  def update_server(self, server: Server):

    # Check desk
    if self.desk.channelChange:
      print("Update Clients: Channels")
      server.send_list("channels", channels_to_JSON(self.desk.channels))
      self.desk.channelChange = False

    if self.desk.inputsChange:
      print("Update Clients: Inputs")
      server.send_list("inputs", inputs_to_JSON(self.desk.inputs))
      self.desk.inputsChange = False
    
    # Check connection
    if (self.deskConnection.connected != self.last_connection) or self.last_connection == None:
      server.send_desk_connected(self.deskConnection.connected)
      self.last_connection = self.deskConnection.connected
      

  def set_default_values(self, messages: List[DeskMessage]):
    for message in messages:
      message.update_desk(self.desk)