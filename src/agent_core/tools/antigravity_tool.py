import logging
import subprocess

class AntigravityTool:
    def __init__(self):
        self.logger = logging.getLogger("agent-core.antigravity")

    def run(self):
        self.logger.info("Antigravity tool invoked")

        try:
            subprocess.run(
                ["wslview", "https://xkcd.com/353/"],
                check=False
            )
        except Exception as e:
            self.logger.warning(f"Browser open skipped: {e}")

