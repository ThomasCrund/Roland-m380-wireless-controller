import React from 'react'
import ChannelSimple from './ChannelSimple'
import ChannelLinked from './ChannelLinked'

export default function ChannelsControl({
  channels = [],
  channelSelected,
  selectChannel,
  log
}) {

  let linkedChannels = []
  return (
    <div style={{ 
      display: 'flex',  
      width: '100vw - 60px',
      overflowX: 'scroll', 
      backgroundColor: '#F0F0FD',
      padding: 10,
      marginLeft: 30,
      marginTop: 15,
      marginBottom: 30,
      marginRight: 30,
      borderRadius: 25
    }}>
      {
        channels ?
        channels.map((channel, index) => {
          if (channel.group != "MAIN") {
            if (channel.properties.link) {
              linkedChannels.push({ group: channel.group,  channelNum: channel.channelNum })
              return <ChannelLinked key={channel.group.toString() + channel.channelNum.toString()} channelSelected={channelSelected} channelA={channel} channelB={channels[index + 1]} log={log} selectChannel={selectChannel} />
            }
            if (linkedChannels.findIndex(c => (channel.group === c.group && channel.channelNum === c.channelNum + 1)) >= 0) {
              return null;
            }  
          }
          return <ChannelSimple key={channel.group.toString() + channel.channelNum.toString()} selected={channel.channelNum === channelSelected} channel={channel} log={log} selectChannel={selectChannel} />
        }) : "No Channels"
      }
    </div>
  )
}
