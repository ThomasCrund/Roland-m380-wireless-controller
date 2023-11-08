import mido

with mido.open_input() as input:
  for msg in input:
    print(msg.bytes())