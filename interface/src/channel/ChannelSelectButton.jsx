import React from 'react'

export default function ChannelSelectButton({
  selected = false,
  colour,
  onClick,
  number = 0
}) {
  return (
    <div style={{ 
      textAlign: 'center', 
      fontSize: 30, 
      backgroundColor: selected ? colour : "transparent",
      color: selected ? "#F0F0FD" : "#0A1128",
      border: `3.5px solid ${colour}`, 
      width: 45, 
      height: 43, 
      borderRadius: 10, 
      paddingTop: 2, 
      userSelect: 'none' ,
      cursor: 'pointer',
}}
onClick={onClick} 
>{number}</div>
  )
}
