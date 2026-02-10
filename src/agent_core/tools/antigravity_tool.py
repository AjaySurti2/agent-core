import logging
import subprocess
from agent_core.tools.base import BaseTool


class AntigravityTool(BaseTool):
    name = "antigravity"
    description = "Launch Antigravity desktop application"
    input_schema = {}
    keywords = ["antigravity", "launch antigravity"]

    def __init__(self):
        self.logger = logging.getLogger("agent-core.antigravity")

    def run(self, **kwargs):
        self.logger.info("Launching Antigravity desktop app")

        try:
            subprocess.run(
                [
                    "cmd.exe",
                    "/c",
                    "start",
                    "",
                    r"C:\Users\ajays\AppData\Local\Programs\Antigravity\Antigravity.exe"
                ],
                check=False
            )

            return "Antigravity desktop app launched"

        except Exception as e:
            self.logger.error(f"Launch failed: {e}")
            return f"Failed to launch Antigravity: {e}"

