from __future__ import annotations
from enum import Enum
from typing import List
import time

class InputSource(Enum):
  REACT_A = "REACT_A"
  REACT_B = "REACT_B"
  CONSOLE = "CONSOLE"
  FX1 = "FX1"
  FX2 = "FX2"
  FX3 = "FX3"
  FX4 = "FX4"
  STEREO_IN = "STEREO_IN"
  PLAY = "PLAY"
  NONE = "NONE"

class InputId:
  def __init__(self, inputSource: InputSource, inputNumber: int):
    self.source = inputSource
    self.number = inputNumber
 
  def __eq__(self, __value: object) -> bool:
    return isinstance(__value, InputId) and (self.source == __value.source) and (self.number == __value.number)

class Input:
  def __init__(self, id: InputId):
    self._id = id
    self._properties = {}

  def set_property(self, property: str, value: int):
    epoch_time = time.time()
    self._properties[property] = { 'value': value, 'timeSet': epoch_time }

  def to_json(self):
    channel_json = {
      'inputId': {
        'inputSource': self._id.source.value,
        'inputNumber': self._id.number,
      },
      'properties': self._properties
    }

    return channel_json
  

def inputs_to_JSON(inputs: List[Input]):
  json = {
    'inputs': [],
    'timeUpdated': time.time()
  }

  for input in inputs:
    json['inputs'].append(input.to_json())

  return json