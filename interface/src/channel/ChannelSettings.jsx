import React, { useEffect, useState } from 'react'
import ChannelSelectButton from './ChannelSelectButton'
import { getChannelColour, inputIdToName } from './ChannelUtil';
import './ChannelSettings.Module.css'
import { socket } from '../socket';

export default function ChannelSettings({
  channel,
  inputsSettings,
  selectChannel
}) {
  const [ name, setName ] = useState(channel.properties.name.map(a => String.fromCharCode(a)).join(''));

  let channelInput = channel.inputId
  let channelColour = getChannelColour(channel.properties.name_color) ?? 0;

  useEffect(() => {
    setName(channel.properties.name.map(a => String.fromCharCode(a)).join(''));
  }, [channel.properties.name])

  let handleUnselect = (e) => {
    selectChannel(0);
  }

  const onChannelInputChange = (e) => {
    let inputSetting = inputsSettings.find(input => inputIdToName(input.inputId) === e.target.value);
    console.log(e.target.value, inputSetting)
    socket.emit('channel-set', 'input', channel.group, channel.channelNum, inputSetting.inputId)
    // setChannelInput(inputSetting.inputId)
  }

  const onChangeNameField = (e) => {
    console.log(e.target.value);
    let newString = e.target.value.substr(0, 6);
    setName(newString);
    let newName = [32, 32, 32, 32, 32];
    for(let i = 0; i < 6; i++) {
      let newNum = e.target.value.charCodeAt(i);
      if (isNaN(newNum)) newNum = 32;
      console.log(newName);
      newName[i] = newNum;
    }
    socket.emit('channel-set', 'name', channel.group, channel.channelNum, newName)
  }



  return (
    <div className='panelsContainer panelsContainerBrief'>
      <div className='panel' style={{ display: 'flex', flexDirection: 'column', width: 180 }}>
        <div style={{ display: 'flex', width: 180, justifyContent: 'center', alignItems: 'center'}}>
          <ChannelSelectButton onClick={handleUnselect} number={channel.channelNum} selected={true} colour={channelColour} />
          <div style={{ marginLeft: 15 }}>
            <input 
              type="text"  
              value={name} 
              onChange={onChangeNameField}
              style={{
                fontSize: 18, 
                color: channelColour,
                width: 80,
                backgroundColor: 'transparent',
                border: 'none'
              }}
            />
          </div>            
        </div>
        <div style={{ display: 'flex', width: 180, justifyContent: 'center', alignItems: 'center' }}>
          <select value={inputIdToName(channelInput)} onChange={onChannelInputChange} className='inputSelect'>
            {inputsSettings.map(input => (
              <option key={inputIdToName(input.inputId)} value={inputIdToName(input.inputId)}>{inputIdToName(input.inputId)}</option>
            ))}
          </select>
        </div>
      </div>
      <div className='panel'>
        Input Panel
      </div>
      <div className='panel'>
        Basic Controls
      </div>
      <div className='panel'>
        Advanced Simple
      </div>


    </div>
  )
}
