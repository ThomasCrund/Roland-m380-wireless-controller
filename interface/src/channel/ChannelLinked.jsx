import React, { useEffect, useState } from 'react'
import { socket } from '../socket';
import Fader from '../util/Fader';
import ChannelSelectButton from './ChannelSelectButton';
import { dBtoSlider, displayDb, faderDbToServer, faderServerToDb, getChannelColour, sliderTodB } from './ChannelUtil';

export default function ChannelLinked(props) {
  const [fader, setFader] = useState(props.channelA.properties.fader ?? [65, 0])
  const [mute, setMute] = useState(props.channelA.properties.mute ?? false)

  const changeFader = (value) => {
    let inputValue = sliderTodB(value);
    let newFader = faderDbToServer((inputValue));
    setFader(newFader)
    socket.emit('channel-set', 'fader', props.channelA.group, props.channelA.channelNum, newFader)
  }

  const changeMute = (e) => {
    let newMute = 1
    if (mute === 1) {
      newMute = 0
    }
    socket.emit('channel-set', 'mute', props.channelA.group, props.channelA.channelNum, newMute)
    setMute(newMute)
  }

  useEffect(() => {
    if (props.channelA.properties.fader != null) {
      setFader(props.channelA.properties.fader)
    } else {
      setFader([64, 0])
    }
    if (props.channelA.properties.mute != null) {
      setMute(props.channelA.properties.mute)
    } else {
      setMute(1)
    }
  }, [props.channelA])

  let channelColourA = getChannelColour(props.channelA.properties.name_color) ?? 0;
  let channelColourB = getChannelColour(props.channelB.properties.name_color) ?? 0;
  let nameA = props.channelA.properties.name ?? [];
  let nameB = props.channelB.properties.name ?? [];

  let muteButtonStylesA = {
    width: 63, 
    height: 25, 
    border: "2px solid " + channelColourA, 
    borderRadius: 5, 
    margin: 5, 
    fontSize: 12,
    display: "flex", 
    justifyContent: "center", 
    alignItems: "center", 
    cursor: 'pointer',
    backgroundColor: mute ? channelColourA : '#F0F0FD',
    color: mute ? 'white' : channelColourA,
    userSelect: 'none',
    marginTop: 8
  }

  let muteButtonStylesB = {
    width: 63, 
    height: 25, 
    border: "2px solid " + channelColourB, 
    borderRadius: 5, 
    margin: 5, 
    fontSize: 12,
    display: "flex", 
    justifyContent: "center", 
    alignItems: "center", 
    cursor: 'pointer',
    backgroundColor: mute ? channelColourB : '#F0F0FD',
    color: mute ? 'white' : channelColourB,
    userSelect: 'none',
    marginTop: 8
  }

  let selectChannelA = (e) => {
    if (props.selected) {
      props.selectChannel(0);
    } else {
      props.selectChannel(props.channelA.channelNum);
    }
  }

  let selectChannelB = (e) => {
    if (props.selected) {
      props.selectChannel(0);
    } else {
      props.selectChannel(props.channelB.channelNum);
    }
  }

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'column', width: 80, alignItems: 'center' }}>
        <ChannelSelectButton onClick={selectChannelA} number={props.channelA.channelNum} selected={props.channelA.channelNum === props.channelSelected} colour={channelColourA} />
        <span onClick={selectChannelA} style={{ color: channelColourA, marginTop: 10, height: 21, cursor: "pointer" }}>{nameA.map(a => String.fromCharCode(a))}</span>
        <div style={muteButtonStylesA} onClick={changeMute}>Mute</div>


        <Fader height={300} value={dBtoSlider(faderServerToDb(fader))} onChange={changeFader} max={1.9} min={100} step={0.1} thumbColor={channelColourA} log={props.log} />
        {displayDb(faderServerToDb(fader))} dB
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', width: 80, alignItems: 'center' }}>
        <ChannelSelectButton onClick={selectChannelB} number={props.channelB.channelNum} selected={props.channelB.channelNum === props.channelSelected} colour={channelColourB} />
        <span onClick={selectChannelB} style={{ color: channelColourB, marginTop: 10, height: 21, cursor: "pointer" }}>{nameB.map(a => String.fromCharCode(a))}</span>
        <div style={muteButtonStylesB} onClick={changeMute}>Mute</div>


        <Fader height={300} value={dBtoSlider(faderServerToDb(fader))} onChange={changeFader} max={1.9} min={100} step={0.1} thumbColor={channelColourB} log={props.log} />
        {displayDb(faderServerToDb(fader))} dB
      </div>
    
    </>
    
  )
}