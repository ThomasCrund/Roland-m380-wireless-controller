import './App.css';
// import useWebSocket, { ReadyState } from 'react-use-websocket';
import React, { useState, useCallback, useEffect } from 'react';
import { socket } from './socket';
import ChannelSimple from './ChannelSimple';

function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [channels, setChannels] = useState([]);
  const [ log, setLog ] = useState({ log: [] });

  useEffect(() => {
    console.log("Register")
    function onConnect() {
      console.log('Connect');
      setIsConnected(true);
    }

    function onDisconnect() {
      console.log('Disconnect');
      setIsConnected(false);
    }

    function onChannels(data) {
      console.log('channels', data)
      setChannels((channels) => data.channels)
    }

    function onInputs(data) {
      console.log('inputs', data)
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('channels', onChannels);
    socket.on('inputs', onInputs);

    return () => {
      console.log("Deregister")
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('faders', onChannels);
      socket.off('inputs', onInputs);
    };
  }, []);

  // const testMouseMove = (e) => {
  //   setObject({
  //     identifier: e.touches[0].identifier, 
  //     x: e.touches[0].pageX,
  //     y: e.touches[0].pageY
  //   });
  // }

  // useEffect(() => {
  //   window.addEventListener('touchstart', testMouseMove)
  //   return () => {
  //     window.addEventListener('touchstart', testMouseMove);
  //   }
  // })

  const addLog = (message) => {
    console.log("Logging:", message);
    setLog(existingLog => {
      console.log(existingLog);
      return { 
        log: [ message, ...existingLog.log ]
      }
    })
  }

  console.log("Channels To print", channels)
  console.log(window.location.host)

  const handleClickSendMessage = useCallback(() => socket.send('Hello'), []);

  return (
    <div style={{
      overflowX: 'hidden',
      overflowY: 'hidden',
      height: '100vh',
      width: '100vw'
    }}>
      <button
        onClick={handleClickSendMessage}
        disabled={!isConnected}
      >
        Click Me to send 'Hello'
      </button>
      Connected: {isConnected ? "Connected" : "Not Connected"}
      <div style={{ 
        display: 'flex',  
        width: '100vw - 60px',
        overflowX: 'scroll', 
        backgroundColor: '#F0F0FD',
        padding: 10,
        marginLeft: 30,
        marginTop: 15,
        marginBottom: 30,
        marginRight: 30,
        borderRadius: 25
      }}>
        {
          channels ?
          channels.map((channel, index) => 
            <ChannelSimple key={channel.group.toString() + channel.channelNum.toString()} channel={channel} log={addLog} />
          ) : "No Channels"
        }
      </div>
      {/* <div style={{ height: 200, width: 700, overflow: 'scroll', backgroundColor: 'white'}}>
        <ul>
          {log.log.map((log) => (<li>{log}</li>))}
        </ul>
      </div> */}
    </div>
  );
}

export default App;
