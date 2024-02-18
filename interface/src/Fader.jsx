import React, { useEffect, useState } from 'react'

export default function Fader({
  value = 0,
  height = 20,
  width = 80,
  min = 0,
  max = 100,
  step = 0.1,
  thumbHeight = 54,
  thumbWidth = 28,
  thumbColor = "#3581B8",
  trackColor = "#C9CAD9",
  trackWidth = 2,
  onChange,
  log
}) {
  const valueToPosition = (num) => {
    return Math.round((num - min) / (max - min) * (height - thumbHeight))
  }

  const [ dragging, setDragging ] = useState(false);
  const [ touchId, setTouchId ] = useState({ id: 0, yLast: 0});
  
  let position = valueToPosition(value);

  const positionToValue = (position) => {
    return Math.round(((position) * (max - min) / (height - thumbHeight) + min) / step ) * step
  }

  const mouseMove = (e) => {
    if (dragging) {
      e.preventDefault();
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
  
  const touchStart = (e) => {
    setTouchId({ id: e.touches[0].identifier, yLast: e.touches[0].pageY });
  }

  const touchEnd = (e) => {
    setTouchId({ id: 0, yLast: 0 });
  }

  const touchMove = (e) => {
    if (touchId.id !== 0) {
      let newPos = position + (e.touches[0].pageY - touchId.yLast);
      if (newPos < 0) newPos = 0;
      if (newPos > (height - thumbHeight)) newPos = (height - thumbHeight);
      onChange(positionToValue(newPos));
      setTouchId(touch => ({ id: touch.id, yLast: e.touches[0].pageY }));
    }
  }

  useEffect(() => {
    // log("Register");
    window.addEventListener('mousemove', mouseMove);
    window.addEventListener('mouseup', mouseUp);
    window.addEventListener('touchend', touchEnd);
    window.addEventListener('touchmove', touchMove)
    return () => {
      // log("Unregister");
      window.removeEventListener('mousemove', mouseMove);
      window.removeEventListener('mouseup', mouseUp);
      window.removeEventListener('touchend', touchEnd);
      window.removeEventListener('touchmove', touchMove);

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
         onTouchStart={touchStart}
         onTouchEnd={touchEnd}
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
