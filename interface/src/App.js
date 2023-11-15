import './App.css';
// import useWebSocket, { ReadyState } from 'react-use-websocket';
import React, { useState, useCallback, useEffect } from 'react';
import { socket } from './socket';

function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);


  useEffect(() => {
    function onConnect() {
      console.log('Connect');
      setIsConnected(true);
    }

    function onDisconnect() {
      console.log('Disconnect');
      setIsConnected(false);
    }

    function onFader(data) {
      console.log('fader', data)
    }

    console.log("Register")
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('channels', onFader);
    socket.on('message', (msg) => {
      console.log("message: " + msg)
    });

    socket.onAny((event, ...args) => {
      console.log(`got ${event}`);
    });

    socket.on("connect_error", (err) => {
      console.log(`connect_error due to ${err.message}`);
    });
    const engine = socket.io.engine;
    engine.on("packet", ({ type, data }) => {
      console.log("packet", type, data)
    });

    engine.once("upgrade", () => {
      // called when the transport is upgraded (i.e. from HTTP long-polling to WebSocket)
      console.log(engine.transport.name); // in most cases, prints "websocket"
    });

    return () => {
      console.log("Deregister")
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('faders', onFader);
    };
  }, []);

  const handleClickSendMessage = useCallback(() => socket.send('Hello'), []);
  
  console.log(isConnected)
  console.log(socket.listenersAny())

  return (
    <div>
      <button
        onClick={handleClickSendMessage}
        disabled={!isConnected}
      >
        Click Me to send 'Hello'
      </button>
      Connected: {isConnected ? "Connected" : "Not Connected"}
    </div>
  );
}

export default App;
