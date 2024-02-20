from typing import List
from web_interface.user_client import User

class UserController:
  def __init__(self) -> None:
    self.users: List[User] = []

  def addUser(self, sid: str):
    self.users.append(User(sid, 1))

  def getSidsMinusOne(self, sid: str):
    sids = []
    for user in self.users:
      if (user.sid != sid):
        sids.append(user.sid)
    return sids