import mido
from typing import List
import time
from message.sysexc_message import SysExcMessage
from message.message import MessageDirection, MessageType

print(mido.get_output_names())
print(mido.get_input_names())

start_byte = 0xF0
manufacture_id = 0x41 # Roland
device_id = 0x10
model_id = [0x00, 0x00, 0x024] # m380 & m400
end_byte = 0xF7

def construct_channel_control_message(channel, value):
    bytes = [channel[0] + 0xB0, channel[1], value]
    return mido.Message.from_bytes(bytes)

def construct_data_request_message(address: List[int], size: List[int]):
    bytes = [start_byte]
    bytes += [manufacture_id]
    bytes += [device_id]
    bytes += model_id
    bytes += [0x11]
    sum = 0
    for byte in address + size:
        sum += byte
    bytes += address
    bytes += size
    odd = sum % 128
    if odd == 0:
        bytes += [0]
    else:
        bytes += [128 - odd]
    bytes += [end_byte]
    return mido.Message.from_bytes(bytes)

def construct_control_message(address: List[int], data: List[int]):
    bytes = [start_byte]
    bytes += [manufacture_id]
    bytes += [device_id]
    bytes += model_id
    bytes += [0x12]
    sum = 0
    for byte in address + data:
        sum += byte
    bytes += address
    bytes += data
    odd = sum % 128
    if odd == 0:
        bytes += [0]
    else:
        bytes += [128 - odd]
    bytes += [end_byte]
    return mido.Message.from_bytes(bytes)

# port = mido.open_output('RSS M-400 1')


# with mido.open_input() as input:
#   for msg in input:
#     print(msg.bytes())
# msg2 = construct_channel_control_message([0, 5], 0)
# msg3 = construct_channel_control_message([0, 5], 50)
# msg4 = construct_channel_control_message([0, 5], 127)
msg = construct_control_message([2, 0, 0, 2], [0x00, 0x00, 0x00, 0x01])
msg2 = SysExcMessage([2, 0, 0, 2], [0x00, 0x00, 0x00, 0x02], [0x00, 0x00, 0x00, 0x01], MessageType.CHANNEL, MessageDirection.SET_TO_HOST)

print(msg.hex())
print(msg2.get_msg().hex())
print(msg2.update_message().get_msg().hex())

# while (True):
#     print('sending')
#     # port.send(msg5)
#     time.sleep(1)
#     port.send(msg2)
#     time.sleep(1)
#     port.send(msg3)
#     time.sleep(1)
#     port.send(msg4)
# #     time.sleep(1)
# #     port.send(msg5)
# #     time.sleep(1)



