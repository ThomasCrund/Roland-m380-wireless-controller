import React from 'react'
import ChannelSelectButton from './ChannelSelectButton'
import { getChannelColour } from './ChannelUtil';

export default function ChannelSettings({
  channel,
  inputsSettings,
  selectChannel
}) {

  let channelColour = getChannelColour(channel.properties.name_color) ?? 0;

  let handleUnselect = (e) => {
    selectChannel(0);
  }



  return (
    <div className='panelsContainer'>
      <div className='panel'>
        <ChannelSelectButton onClick={handleUnselect} number={channel.channelNum} selected={true} colour={channelColour} />

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
