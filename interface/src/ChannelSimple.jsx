

import React, { useEffect, useState } from 'react'
import { socket } from './socket';
import Fader from './Fader';

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
    if (mod === 128) {
      mod = 0;
      times = times += 1;
      if (times === 128) {
        times = 0;
      }
    } 
    return [times, mod];
  }
}

function mapValues(x, in_min, in_max, out_min, out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function dBtoSlider(dB) {
  if (dB >= -10.0) return mapValues(dB, -10.0, 10.0, 60, 100);
  if (dB >= -40.0) return mapValues(dB, -40.0, -10, 20, 60);
  if (dB >= -50.0) return mapValues(dB, -50.0, -40, 12, 20);
  if (dB >= -60.0) return mapValues(dB, -60.0, -50, 7, 12);
  if (dB >= -80.0) return mapValues(dB, -80.0, -60, 2, 7);
  return 1.9;
}

function sliderTodB(dB) {
  if (dB >= 60) return mapValues(dB, 60, 100, -10.0, 10.0);
  if (dB >= 20) return mapValues(dB, 20, 60, -40.0, -10);
  if (dB >= 12) return mapValues(dB, 12, 20, -50.0, -40);
  if (dB >= 7) return mapValues(dB, 7, 12, -60.0, -50);
  if (dB >= 2) return mapValues(dB, 2, 7, -80.0, -60);
  return -Number.MAX_VALUE;
}

function displayDb(dB) {
  if (dB === -Number.MAX_VALUE) {
    return "-INF";
  } else {
    return String(dB);
  }
}

function getChannelColour(name_colour) {
  switch (name_colour) {
    case 0: // Navy
      return '#001F54';
    case 1: // Blue
      return '#3581B8';
    case 2: // Brown
      return '#DE6449'
    case 3: // Red
      return '#931621';
    case 4: // Yellow
      return '#FDCA40';
    case 5: // Green
      return '#09BC8A';
    case 6: // Aqua
      return '#44E5E7';
    case 7: // Purple
      return '#791E94';
    default:
      return '#FFFFFF';
  }
}

export default function ChannelSimple(props) {
  const [fader, setFader] = useState(props.channel.properties.fader ?? [65, 0])
  const [mute, setMute] = useState(props.channel.properties.mute ?? false)
  // console.log(props)
  const changeFader = (value) => {
    let inputValue = sliderTodB(value);
    let newFader = faderDbToServer((inputValue));
    console.log(inputValue, newFader)
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
    } else {
      setFader([64, 0])
    }
    if (props.channel.properties.mute != null) {
      setMute(props.channel.properties.mute)
    } else {
      setMute(1)
    }
  }, [props.channel])

  let channelColour = getChannelColour(props.channel.properties.name_color) ?? 0;
  let name = props.channel.properties.name ?? [];

  let muteButtonStyles = {
    width: 40, 
    height: 25, 
    border: "2px solid " + channelColour, 
    borderRadius: 5, 
    margin: 5, 
    fontSize: 15,
    display: "flex", 
    justifyContent: "center", 
    alignItems: "center", 
    cursor: 'pointer',
    backgroundColor: mute ? channelColour : 'white',
    color: mute ? 'white' : channelColour
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 80, alignItems: 'center' }}>
      <div style={{ width: '100%', textAlign: 'center', fontSize: 20, color: channelColour }}>{props.channel.channelNum}</div>
      <span style={{ color: channelColour }}>{name.map(a => String.fromCharCode(a))}</span>
      <div style={muteButtonStyles} onClick={changeMute}>Mute</div>


      <Fader height={400} value={dBtoSlider(faderServerToDb(fader))} onChange={changeFader} max={1.9} min={100} step={0.1} thumbColor={channelColour} />
      {displayDb(faderServerToDb(fader))} dB
    </div>
  )
}