import React from 'react'

export default function PropertySwitch({
  onClick = () => {},
  selected = false,
  width = 60,
  height = 20,
  color = '#0A1128',
  label = "Button"
}) {
  return (
    <div
      style={{
        width,
        height,
        border: `2px solid ${color}`,
        backgroundColor: selected ? color : 'transparent',
        borderRadius: 5,
        textAlign: 'center',
        marginTop: 3,
        marginBottom: 3,
        color: selected ? '#F0F0FD' : color 
      }}
      onClick={onClick}
    >
      {label}
    </div>
  )
}
