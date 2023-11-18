

import React, { useEffect, useState } from 'react'
import { socket } from './socket';

export default function ChannelSimple(props) {
  const [fader, setFader] = useState(props.channel.fader ?? 0)
  const [mute, setMute] = useState(props.channel.mute ?? false)
  // console.log(props)
  const changeFader = (e) => {
    setFader(e.target.value)
    socket.emit('channel-fader-set', props.channel.group, props.channel.channelNum, Number(e.target.value))
  }

  const changeMute = (e) => {
    socket.emit('channel-mute-set', props.channel.group, props.channel.channelNum, !mute)
    setMute(!mute)
  }

  useEffect(() => {
    if (props.channel.fader != null) {
      setFader(props.channel.fader)
    }
  }, [props.channel])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 40}}>
      <div style={{ width: '100%', textAlign: 'center', fontSize: 20}}>{props.channel.channelNum}</div> 
      <div style={{ width: '100%', textAlign: 'center', fontSize: 20}}>{props.channel.mute}</div> 
      <input type="checkbox" onChange={changeMute} value={mute} />
      <input type="range" min="0" max="127"  value={fader} style={{ appearance: 'slider-vertical', height: 300 }} onChange={changeFader}/>
      {props.channel.mute}
    </div>
  )
}
