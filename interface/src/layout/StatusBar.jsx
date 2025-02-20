import React from 'react'

function StatusBar({
  status
}) {

  console.log(status)
  return (
    <div style={{
      width: '100%',
      height: 55,
      backgroundColor: "#C9CAD9",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    }}
    >
    <div>
      

    </div>

    <div style={{
      display: "flex"
    }}>
      
        <div style={{
        width: 30,
        height: 30,
        display: 'flex',
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: (status?.reactA ?? false) ? "#9BC7C6" : "#D4B0B4",
        borderRadius: 15,
        marginRight: 15
      }}>
        A   
      </div>
      <div style={{
        width: 30,
        height: 30,
        display: 'flex',
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: (status?.reactB ?? false) ? "#9BC7C6" : "#D4B0B4",
        borderRadius: 15,
        marginRight: 15
      }}>
        B
      </div>
      <div style={{
        width: 30,
        height: 30,
        display: 'flex',
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: (status?.deskConnected ?? false) ? "#9BC7C6" : "#D4B0B4",
        borderRadius: 15,
        marginRight: 15
      }}>
        <svg xmlns="http://www.w3.org/2000/svg" width={20} height={16} viewBox="0 0 640 512">{/*Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.*/}<path d="M641.5 256c0 3.1-1.7 6.1-4.5 7.5L547.9 317c-1.4 .8-2.8 1.4-4.5 1.4-1.4 0-3.1-.3-4.5-1.1-2.8-1.7-4.5-4.5-4.5-7.8v-35.6H295.7c25.3 39.6 40.5 106.9 69.6 106.9H392V354c0-5 3.9-8.9 8.9-8.9H490c5 0 8.9 3.9 8.9 8.9v89.1c0 5-3.9 8.9-8.9 8.9h-89.1c-5 0-8.9-3.9-8.9-8.9v-26.7h-26.7c-75.4 0-81.1-142.5-124.7-142.5H140.3c-8.1 30.6-35.9 53.5-69 53.5C32 327.3 0 295.3 0 256s32-71.3 71.3-71.3c33.1 0 61 22.8 69 53.5 39.1 0 43.9 9.5 74.6-60.4C255 88.7 273 95.7 323.8 95.7c7.5-20.9 27-35.6 50.4-35.6 29.5 0 53.5 23.9 53.5 53.5s-23.9 53.5-53.5 53.5c-23.4 0-42.9-14.8-50.4-35.6H294c-29.1 0-44.3 67.4-69.6 106.9h310.1v-35.6c0-3.3 1.7-6.1 4.5-7.8 2.8-1.7 6.4-1.4 8.9 .3l89.1 53.5c2.8 1.1 4.5 4.1 4.5 7.2z"/></svg>      </div>
      <div style={{
        width: 30,
        height: 30,
        display: 'flex',
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: (status?.connected ?? false) ? "#9BC7C6" : "#D4B0B4",
        borderRadius: 15,
        marginRight: 15
      }}>
        <svg xmlns="http://www.w3.org/2000/svg" width={20} height={16} viewBox="0 0 640 512">{/*Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.*/}<path d="M54.2 202.9C123.2 136.7 216.8 96 320 96s196.8 40.7 265.8 106.9c12.8 12.2 33 11.8 45.2-.9s11.8-33-.9-45.2C549.7 79.5 440.4 32 320 32S90.3 79.5 9.8 156.7C-2.9 169-3.3 189.2 8.9 202s32.5 13.2 45.2 .9zM320 256c56.8 0 108.6 21.1 148.2 56c13.3 11.7 33.5 10.4 45.2-2.8s10.4-33.5-2.8-45.2C459.8 219.2 393 192 320 192s-139.8 27.2-190.5 72c-13.3 11.7-14.5 31.9-2.8 45.2s31.9 14.5 45.2 2.8c39.5-34.9 91.3-56 148.2-56zm64 160a64 64 0 1 0 -128 0 64 64 0 1 0 128 0z"/></svg>
      </div>

    </div>
    </div>
  )
}

export default StatusBar