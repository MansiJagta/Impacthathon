class BaseAgent:
    """Base class for all processing agents."""

    def run(self, state: dict) -> dict:
        raise NotImplementedError
