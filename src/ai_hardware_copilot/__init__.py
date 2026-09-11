"""AI Hardware Copilot engineering-conference runtime."""

from .conference import ConferenceEngine
from .directory import AgentDirectory
from .models import ConferenceState, TaskManifest

__all__ = ["AgentDirectory", "ConferenceEngine", "ConferenceState", "TaskManifest"]
__version__ = "0.1.0"

