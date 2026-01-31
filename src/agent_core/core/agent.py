import logging
import signal
import sys

class Agent:
    def __init__(self, name: str):
        self.name = name
        self.running = False
        self.logger = logging.getLogger(self.name)

    def setup(self):
        """Initialize tools, memory, config"""
        pass

    def step(self):
        raise NotImplementedError

    def shutdown(self):
        self.logger.info("shutdown initiated")
        self.running = False

    def _handle_signal(self, signum, frame):
        self.logger.info(f"received signal {signum}")
        self.shutdown()

    def run(self):
        self.running = True

        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        self.setup()
        self.logger.info("agent started")

        while self.running:
            self.step()

        self.logger.info("agent stopped")
