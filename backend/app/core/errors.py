class PitchPilotError(Exception):
    """Base exception for PitchPilot"""
    pass

class LLMInvalidOutput(PitchPilotError):
    """Raised when the LLM returns output that cannot be parsed or validated (Maps to 502)"""
    pass

class LLMUnavailable(PitchPilotError):
    """Raised when all LLM providers fail or timeout (Maps to 503)"""
    pass
