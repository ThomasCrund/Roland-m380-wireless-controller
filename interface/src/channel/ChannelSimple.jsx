

import React, { useEffect, useState } from 'react'
import { socket } from '../socket';
import Fader from '../util/Fader';
import ChannelSelectButton from './ChannelSelectButton';
import { dBtoSlider, displayDb, faderDbToServer, faderServerToDb, getChannelColour, sliderTodB } from './ChannelUtil';

export default function ChannelSimple(props) {
  const [fader, setFader] = useState(props.channel.properties.fader ?? [65, 0])
  const [mute, setMute] = useState(props.channel.properties.mute ?? false)

  const changeFader = (value) => {
    let inputValue = sliderTodB(value);
    let newFader = faderDbToServer((inputValue));
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
    width: 63, 
    height: 25, 
    border: "2px solid " + channelColour, 
    borderRadius: 5, 
    margin: 5, 
    fontSize: 12,
    display: "flex", 
    justifyContent: "center", 
    alignItems: "center", 
    cursor: 'pointer',
    backgroundColor: mute ? channelColour : '#F0F0FD',
    color: mute ? 'white' : channelColour,
    userSelect: 'none',
    marginTop: 8
  }

  let selectChannel = (e) => {
    if (props.selected) {
      props.selectChannel(0);
    } else {
      props.selectChannel(props.channel.channelNum);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: 80, alignItems: 'center' }}>
      <ChannelSelectButton onClick={selectChannel} number={props.channel.channelNum} selected={props.selected} colour={channelColour} />
      <span onClick={selectChannel} style={{ color: channelColour, marginTop: 10, height: 21, cursor: "pointer" }}>{name.map(a => String.fromCharCode(a))}</span>
      <div style={muteButtonStyles} onClick={changeMute}>Mute</div>


      <Fader height={300} value={dBtoSlider(faderServerToDb(fader))} onChange={changeFader} max={1.9} min={100} step={0.1} thumbColor={channelColour} log={props.log} />
      {displayDb(faderServerToDb(fader))} dB
    </div>
  )
}