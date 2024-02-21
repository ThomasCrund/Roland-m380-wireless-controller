import React, { useEffect, useState } from 'react'
import PropertyControl, { PropertyDivider } from '../../util/PropertyControl';
import { gainToDb, getChannelColour } from '../ChannelUtil';
import { socket } from '../../socket';
import PropertySwitch from '../../util/PropertySwitch';

export default function InputBoardPanel({
  channel,
  inputsSettings
}) {

  let input = inputsSettings.find(input => input.inputId.inputSource === channel.inputId.inputSource && input.inputId.inputNumber === channel.inputId.inputNumber);

  console.log(input)

  const [ gain, setGain ] = useState(input.properties.gain);
  const [ pad, setPad ] = useState(input.properties.pad);
  const [ phantom, setPhantom ] = useState(input.properties.phantom);
  const [ link, setLink ] = useState(input.properties.link);
  
  let channelColour = getChannelColour(channel.properties.name_color) ?? 0;

  useEffect(() => {
    let input = inputsSettings.find(input => input.inputId.inputSource === channel.inputId.inputSource && input.inputId.inputNumber === channel.inputId.inputNumber);
    setGain(input.properties.gain)
  }, [inputsSettings, channel])

  let gainChange = (amount) => {
    let newGain = gain + amount;
    if (newGain > 55) newGain = 55
    else if (newGain < 0) newGain = 0
    setGain(newGain)
    socket.emit('input-set', 'gain', input.inputId.inputSource, input.inputId.inputNumber, Math.round(newGain), false)

  }

  return (
    <div className='panel' style={{ display: 'flex', flexDirection: 'row', width: 'min-content' }}>
      <PropertyControl color={channelColour} label="Gain" value={gain} textValue={gainToDb(gain, pad) + " dB"} onChange={gainChange} min={0} max={55} />
      <PropertyDivider />
      <div style={{ width: 60, height: 80}}>
        <PropertySwitch label='Pad' selected={pad} />
        <PropertySwitch label='+48V' selected={phantom} />
        <PropertySwitch label='Link' selected={link} />
      </div>
    </div>
  )
}
