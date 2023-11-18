import './App.css';
// import useWebSocket, { ReadyState } from 'react-use-websocket';
import React, { useState, useCallback, useEffect } from 'react';
import { socket } from './socket';
import ChannelSimple from './ChannelSimple';

function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [channels, setChannels] = useState([]);

  useEffect(() => {
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
      setChannels(data.channels)
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('channels', onChannels);



    return () => {
      console.log("Deregister")
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('faders', onChannels);
    };
  }, []);

  console.log("Channels To print", channels)
  console.log(window.location.host)

  const handleClickSendMessage = useCallback(() => socket.send('Hello'), []);

  return (
    <div>
      <button
        onClick={handleClickSendMessage}
        disabled={!isConnected}
      >
        Click Me to send 'Hello'
      </button>
      Connected: {isConnected ? "Connected" : "Not Connected"}
      <div style={{ display: 'flex' }}>
        {
          channels ?
          channels.map((channel, index) => 
            <ChannelSimple key={channel.group.toString() + channel.channelNum.toString()} channel={channel} />
          ) : "No Channels"
        }
      </div>
    </div>
  );
}

export default App;
