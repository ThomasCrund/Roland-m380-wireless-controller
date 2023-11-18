# Roland M380/M400 Wireless controller

To remotely control the Roland M380 and M400 sound desks from an Ipad using a raspberry Pi or computer connected to the sound desk of the MIDI interface.

## How it works

Consists of two modules, the server which communicates between the website interface and the sound desk and the interface which allow the users to modify and read sound desk values

### Server

Written in python this module uses mido and rtmidi to communicate over MIDI to the sound desk, It then stores the state of the sound desk and communicates that bi-directionally between the desk and the interface using flask and flask-socketio

### Interface

Written in react this uses the socket-io library to communicate with the socket io server. The Interface is located in the [./interface](./interface) directory 

## Installation

TODO Properly, in short:
- Create a virtual python environment
- Install Dependencies (look into rtmidi, that is more complicated)
- to run server run `python server/main.py`
- cd into interface and `run npm start`


## Contributors

- @ThomasCrund  