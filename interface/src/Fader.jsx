import React, { useEffect, useState } from 'react'

export default function Fader({
  value = 0,
  height = 300,
  width = 80,
  min = 0,
  max = 100,
  step = 0.1,
  thumbHeight = 54,
  thumbWidth = 28,
  thumbColor = "#3581B8",
  trackColor = "#C9CAD9",
  trackWidth = 2,
  onChange
}) {
  const valueToPosition = (num) => {
    return Math.round((num - min) / (max - min) * (height - thumbHeight))
  }

  const [ dragging, setDragging ] = useState(false);
  
  let position = valueToPosition(value);

  const positionToValue = (position) => {
    return Math.round(((position) * (max - min) / (height - thumbHeight) + min) / step ) * step
  }

  const mouseMove = (e) => {
    if (dragging) {
      let newPos = position + e.movementY
      if (newPos < 0) newPos = 0;
      if (newPos > (height - thumbHeight)) newPos = (height - thumbHeight);
      console.log(newPos, valueToPosition(positionToValue(newPos)), positionToValue(newPos))
      onChange(positionToValue(newPos))

    }
  }

  const mouseUp = (e) => {
    if (dragging) {
      setDragging(false)
    }
  }

  useEffect(() => {
    window.addEventListener('mousemove', mouseMove);
    window.addEventListener('mouseup', mouseUp)

    return () => {
      window.removeEventListener('mousemove', mouseMove);
      window.removeEventListener('mouseup', mouseUp)
    }
  })



  return (
    <div className='fader-container'
         style={{
          height,
          width,
          display: 'flex',
          userSelect: 'none',
         }}
         onMouseDown={e => setDragging(true)}
         onMouseUp={e => setDragging(false)}
    >
      <div className='fader-track'
           style={{
            width: trackWidth,
            position: 'relative',
            height: '100%',
            backgroundColor: trackColor,
            transform: `translateX(${width / 2 - trackWidth / 2}px)`
           }}></div>
      <div className='fader-thumb'
           style={{
            backgroundColor: thumbColor,
            width: thumbWidth,
            height: thumbHeight,
            position: 'relative',
            transform: `translateY(${position}px) translateX(${width / 2 - trackWidth - thumbWidth / 2}px)`,
            borderRadius: 10
           }}></div>
    </div>
  )
}
