from desk import Channel, ChannelId
from typing import List
import time

def channels_to_JSON(channels: List[Channel]):
  json = {
    'channels': [],
    'timeUpdated': time.time()
  }

  for channel in channels:
    channel_json = {
      'fader': channel.fader,
      'mute': channel.mute,
      'group': channel._id.group.value,
      'channelNum': channel._id.deskChannel
    }
    json['channels'].append(channel_json)

  return json
