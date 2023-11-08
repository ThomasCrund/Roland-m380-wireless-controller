from app import App
import signal

if __name__ == "__main__":
  app = App()
  signal.signal(signal.SIGINT, app.exit_application)
  app.run()