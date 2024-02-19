import React from 'react'
import ChannelSimple from './ChannelSimple'

export default function ChannelsControl({
  channels = [],
  channelSelected,
  selectChannel,
  log
}) {
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
          return <ChannelSimple key={channel.group.toString() + channel.channelNum.toString()} selected={channel.channelNum === channelSelected} channel={channel} log={log} selectChannel={selectChannel} />
        }) : "No Channels"
      }
    </div>
  )
}
