import './App.css';
// import useWebSocket, { ReadyState } from 'react-use-websocket';
import React, { useState, useCallback, useEffect } from 'react';
import { socket } from './socket';
import ChannelSimple from './channel/ChannelSimple';
import ChannelsControl from './channel/ChannelsControl';
import ChannelSettings from './channel/ChannelSettings';

function App() {
  const [ connection, setConnection] = useState({ connected: false });
  const [ channels, setChannels ] = useState([]);
  const [ inputs, setInputs ] = useState([]);
  const [ channelSelected, setChannelSelected ] = useState(0)
  const [ log, setLog ] = useState({ log: [] });

  useEffect(() => {
    console.log("Register")
    function onConnect() {
      console.log('Connect');
      setConnection(oldCon => ({ ...oldCon, connected: true }));
    }

    function onDisconnect() {
      console.log('Disconnect');
      setConnection(oldCon => ({ ...oldCon, connected: true }));
    }

    function onChannels(data) {
      console.log('channels', data)
      setChannels((channels) => data.channels)
    }

    function onInputs(data) {
      console.log('inputs', data)
      setInputs((inputs) => data.inputs)
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

  const addLog = (message) => {
    console.log("Logging:", message);
    setLog(existingLog => {
      console.log(existingLog);
      return { 
        log: [ message, ...existingLog.log ]
      }
    })
  }

  const selectChannel = (faderNum) => {
    setChannelSelected(faderNum)
  }

  return (
    <div style={{
      overflowX: 'hidden',
      overflowY: 'hidden',
      height: '100vh',
      width: '100vw'
    }}>
      {/* Connected: {isConnected ? "Connected" : "Not Connected"} */}
      {
        channelSelected !== 0 
        ? <ChannelSettings channel={channels.find(channel => channel.group === "FADER" && channel.channelNum === channelSelected)} selectChannel={selectChannel} inputsSettings={inputs} /> 
        : null
      }
      <ChannelsControl channels={channels} log={addLog} selectChannel={selectChannel} channelSelected={channelSelected} />
    </div>
  );
}

export default App;
