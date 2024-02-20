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
  const [ showNameColour, setShowNameColour ] = useState(false);

  let channelInput = channel.inputId
  let channelColour = getChannelColour(channel.properties.name_color) ?? 0;

  useEffect(() => {
    let newName = channel.properties.name.map(a => String.fromCharCode(a)).join('').trimEnd();
    setName(newName);
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
    socket.emit('channel-set', 'name', channel.group, channel.channelNum, newName, false)
  }

  const onNameLoseFocus = (e) => {
    let newName = [32, 32, 32, 32, 32];
    for(let i = 0; i < 6; i++) {
      let newNum = e.target.value.charCodeAt(i);
      if (isNaN(newNum)) newNum = 32;
      console.log(newName);
      newName[i] = newNum;
    }
    socket.emit('channel-set', 'name', channel.group, channel.channelNum, newName, true)

  }

  let closeModal = (e) => {
    console.log(e.target.id, e.target.class)
    if (!(e.target.id === 'name-input' || e.target.id === 'nameColourModal')) {
      setShowNameColour(false)
    }
  }

  let setColour = (num) => {
    socket.emit('channel-set', 'name_color', channel.group, channel.channelNum, num, true)
  }

  useEffect(() => {
    document.addEventListener('click', closeModal);

    return () => {
      document.removeEventListener('click', closeModal);
    }
  })

  console.log(showNameColour)

  return (
    <div className='panelsContainer panelsContainerBrief'>
      <div className='panel' style={{ display: 'flex', flexDirection: 'column', width: 180 }}>
        <div style={{ display: 'flex', width: 180, justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
          <ChannelSelectButton onClick={handleUnselect} number={channel.channelNum} selected={true} colour={channelColour} />
          <div style={{ marginLeft: 15 }}>
            <input 
              type="text"
              id='name-input'  
              value={name} 
              onChange={onChangeNameField}
              onSelect={e => setShowNameColour(true)}
              onBlur={onNameLoseFocus}
              style={{
                fontSize: 18, 
                color: channelColour,
                width: 80,
                backgroundColor: 'transparent',
                border: 'none'
              }}
            />
          </div>
          <div
            style={{
              display: showNameColour ? 'grid' : 'none',
              position: 'absolute',
              zIndex: 2,
              backgroundColor: 'white',
              padding: 5,
              paddingBottom: 0,
              borderRadius: 5,
              top: 40,
              gridTemplateColumns: '20px 20px 20px 20px',
              gridTemplateRows: '20px 20px',
            }}
            id='nameColourModal'
          >
            {
              [0, 1, 2, 3, 4, 5, 6, 7].map(colourNumber => (
                <div
                  style={{
                    width: 15,
                    height: 15,
                    backgroundColor: getChannelColour(colourNumber),
                    cursor: 'pointer'
                  }}
                  onClick={e => setColour(colourNumber)}
                ></div>
              ))
            }
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
