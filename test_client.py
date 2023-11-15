import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
while True:
  time.sleep(3)
  print("sending to 'my_message': 'test")
  sio.emit('my_message', 'test')
