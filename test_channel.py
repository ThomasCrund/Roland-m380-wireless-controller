from src.desk.channel import ChannelId, Group

def print_channelId(channelId: ChannelId):
  print(channelId.group, channelId.deskChannel, hex(channelId.get_MIDI_channel()), hex(channelId.get_MIDI_controller()))

def main():
  a = ChannelId(Group.FADER, 5)
  print_channelId(a)
  b = ChannelId.from_control_message_bytes([0xBF, 0x01])
  print_channelId(b)
  c = ChannelId.from_control_message_bytes([0xB0, 0x05])
  print_channelId(c)
  print(a == b)
if __name__ == '__main__':
  main()