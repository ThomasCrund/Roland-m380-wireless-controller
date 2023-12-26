from desk.channel import ChannelId, Group
from message import MessageController
from message.fader_message import FaderMessage
from message.mute_message import MuteMessage

def print_channelId(channelId: ChannelId):
  print(channelId.group, channelId.deskChannel, hex(channelId.get_MIDI_channel()), hex(channelId.get_MIDI_controller()))

def main():
  # a = ChannelId(Group.FADER, 5)
  # print_channelId(a)
  # b = ChannelId.from_control_message_bytes([0xBF, 0x01])
  # print_channelId(b)
  # c = ChannelId.from_control_message_bytes([0xB0, 0x05])
  # print_channelId(c)
  # print(a == c)

  mc = MessageController()

  fad = FaderMessage(ChannelId(Group.FADER, 5), 50)
  mut = MuteMessage(ChannelId(Group.FADER, 5), 50)

  fad2 = mc.interpret_message_from_bytes(fad.bytes())
  mut2 = mc.interpret_message_from_bytes(mut.bytes())

  print(fad2 == fad)
  print(mut2 == mut)
  print(mut2 == fad)




if __name__ == '__main__':
  main()