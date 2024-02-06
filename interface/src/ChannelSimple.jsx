

import React, { useEffect, useState } from 'react'
import { socket } from './socket';

function faderServerToDb(fader) {
  if (fader[0] === 0) {
    return Math.round(fader[1]) / 10;
  } else if (fader[0] > 120) {
    return Math.round(((fader[1] * 0.1) - (128 - fader[0]) * 12.8) * 10) / 10;
  } else if (fader[0] === 64) {
    return -Number.MAX_VALUE;
    // return -81;
  }
}

function faderDbToServer(dB) {
  if (dB > 10) {
    throw RangeError(`dB Value: ${dB} is greater than max dB 10.0`);
  } else if (dB === -Number.MAX_VALUE) {
    return [64, 0]
  } else if (dB >= 0.0) {
    return [0, Math.round(dB * 10)]
  } else if (dB < -80) {
    throw RangeError(`dB Value: ${dB} is less than min dB -80.0`);
  } else {
    let mod = 128 - Math.round( - (dB % 12.8) * 10);
    let times = 127 - Math.floor(dB / -12.8);
    return [times, mod];
  }
}

function displayDb(dB) {
  if (dB === -Number.MAX_VALUE) {
    return "-INF";
  } else {
    return String(dB);
  }
}

export default function ChannelSimple(props) {
  const [fader, setFader] = useState(props.channel.properties.fader ?? [65, 0])
  const [mute, setMute] = useState(props.channel.properties.mute ?? false)
  // console.log(props)
  const changeFader = (e) => {
    let inputValue = e.target.value;
    if (inputValue < -80.0) inputValue = -Number.MAX_VALUE;
    let newFader = faderDbToServer(inputValue);
    setFader(newFader)
    socket.emit('channel-set', 'fader', props.channel.group, props.channel.channelNum, newFader)
  }

  const changeMute = (e) => {
    let newMute = 1
    if (mute === 1) {
      newMute = 0
    }
    socket.emit('channel-set', 'mute', props.channel.group, props.channel.channelNum, newMute)
    setMute(newMute)
  }

  useEffect(() => {
    if (props.channel.properties.fader != null) {
      setFader(props.channel.properties.fader)
    }
    if (props.channel.properties.mute != null) {
      setMute(props.channel.properties.mute)
    }
  }, [props.channel])

  let muteButtonStyles = {
    width: 40, 
    height: 25, 
    border: "1px solid black", 
    borderRadius: 5, 
    margin: 5, 
    fontSize: 15,
    display: "flex", 
    justifyContent: "center", 
    alignItems: "center", 
    cursor: 'pointer',
    backgroundColor: mute ? 'black' : 'white',
    color: mute ? 'white' : 'black'
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 50 }}>
      <div style={{ width: '100%', textAlign: 'center', fontSize: 20 }}>{props.channel.channelNum}</div>
      <div style={{ width: '100%', textAlign: 'center', fontSize: 20 }}>{props.channel.mute}</div>
      <div style={muteButtonStyles} onClick={changeMute}>Mute</div>
      <div style={muteButtonStyles} onClick={changeMute}>{0}</div>
      
      <input type="range" min="-80.1" max="10.0" step="0.1" value={faderServerToDb(fader)} style={{ appearance: 'slider-vertical', height: 300 }} onChange={changeFader} />
      {displayDb(faderServerToDb(fader))} dB
    </div>
  )
}