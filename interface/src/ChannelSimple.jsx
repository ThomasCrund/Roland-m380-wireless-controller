

import React, { useEffect, useState } from 'react'
import { socket } from './socket';

export default function ChannelSimple(props) {
  const [fader, setFader] = useState(props.channel.fader ?? 0)
  // console.log(props)
  const changeFader = (e) => {
    setFader(e.target.value)
    socket.emit('channel-fader-set', props.channel.group, props.channel.channelNum, Number(e.target.value))
  }

  useEffect(() => {
    if (props.channel.fader != null) {
      setFader(props.channel.fader)
    }
  }, [props.channel])

  return (
    <div>
      <div>{props.channel.group}-{props.channel.channelNum}:</div> 
      <input type="range" min="0" max="127" value={fader} onChange={changeFader}/>
    </div>
  )
}
