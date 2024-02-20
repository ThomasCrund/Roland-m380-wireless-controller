import React, { useEffect, useState } from 'react'
import ChannelSelectButton from './ChannelSelectButton'
import { getChannelColour, inputIdToName } from './ChannelUtil';
import './ChannelSettings.css'
import { socket } from '../socket';
import NameInput from './panel/NameInput';

export default function ChannelSettings({
  channel,
  inputsSettings,
  selectChannel
}) {


  return (
    <div className='panelsContainer panelsContainerBrief'>
      <NameInput channel={channel} inputsSettings={inputsSettings} selectChannel={selectChannel} />
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
