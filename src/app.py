from src.server import Server
import time

class App:

  def __init__(self):
    self.server = Server()

  def run(self):
    print("Starting App")
    self.server.start()
    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      print("End Logger")

  def exit_application(self, num, stack):
    print("Closing App")
    # self.server.end()
    exit()



    