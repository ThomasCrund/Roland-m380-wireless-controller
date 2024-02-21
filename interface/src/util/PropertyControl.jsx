import React, { useEffect, useState } from 'react'
import { mapValues } from '../channel/ChannelUtil';

export default function PropertyControl({
  value,
  textValue = value,
  onChange = (amount) => console.log("Not Implemented", amount),
  verticalRate = 0.1,
  horizontalRate = 0.2,
  label,
  min = 0,
  max = 100,
  width = 60,
  height = 80,
  color
}) {

  const [ mouseDragging, setMouseDragging ] = useState(false);
  const [ touch, setTouch ] = useState({ touchId: 0, touching: false, lastPos: {x: 0, y: 0}})
  const [ log, setLog ] = useState([]);

  const addLog = (message) => {
    setLog(log => [message, ...log])
  }

  let mouseDown = (e) => {
    setMouseDragging(true);
  }

  let mouseUp = (e) => {
    setMouseDragging(false);
  }

  let mouseMove = (e) => {
    if (mouseDragging) {
      console.log()
      let changeAmount = (-e.movementY * verticalRate) + (e.movementX * horizontalRate);
      onChange(changeAmount);
    }
  }

  const touchStart = (e) => {
    setTouch({ touching: true, id: e.touches[0].identifier, lastPos: {x: e.touches[0].pageX, y: e.touches[0].pageY} });
  }

  const touchEnd = (e) => {
    setTouch({ id: 0, touching: false, lastPos: {x: 0, y: 0} });
  }

  const touchMove = (e) => {
    if (touch.touching) {
      e.preventDefault();
      addLog("last y: " + touch.lastPos.y + ", x: " + touch.lastPos.x);
      let changeAmount = (-(e.touches[0].pageY - touch.lastPos.y) * verticalRate) + ((e.touches[0].pageX - touch.lastPos.x) * horizontalRate);
      onChange(changeAmount);
      setTouch({ touching: true, id: e.touches[0].identifier, lastPos: {x: e.touches[0].pageX, y: e.touches[0].pageY} });
    }
  }

  useEffect(() => {
    window.addEventListener('mousemove', mouseMove);
    window.addEventListener('mouseup', mouseUp);
    window.addEventListener('touchend', touchEnd);
    window.addEventListener('touchmove', touchMove)
    return () => {
      window.removeEventListener('mousemove', mouseMove);
      window.removeEventListener('mouseup', mouseUp);
      window.removeEventListener('touchend', touchEnd);
      window.removeEventListener('touchmove', touchMove);

    }
  })

  return (
    <div
      style={{
        width,
        height,
        userSelect: 'none',
        overflow: 'hidden',
        touchAction: 'none',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}
      onMouseDown={mouseDown}
      onTouchStart={touchStart}
    >
      <div 
        style={{
          fontSize: 20,
        }}
      >{label}</div>

      <div
        style={{
          width: width-8,
          height: 15,
          border: `1px solid #0A1128`,
          borderRadius: 5,
          overflow: 'hidden',
          marginTop: 5,
        }}
      >
        <div
          style={{
            position: 'relative',
            height: 15,
            width: 0,
            border: `2px solid ${color}`,
            left: mapValues(value, min, max, -2, width-10)
          }}></div>
      </div>

      {textValue}      
    </div>
  )
}


export function PropertyDivider({
  height = 80,
  color = '#C3C3CD',
  marginSide = 7
}) {
  return (
    <div 
      style={{
        height,
        width: 0,
        border: `2px solid ${color}`,
        marginLeft: marginSide,
        marginRight: marginSide,
        borderRadius: 4
      }}
    ></div>
  )
}