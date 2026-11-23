"""Stand-in for a partner agency's package. We rent out their vans too.

Treat this file as a library we can't change: same in before/ and after/.
"""

from datetime import date


class LeasedVan:
    def __init__(self, registration: str, euros_per_day: float) -> None:
        self.registration = registration
        self.euros_per_day = euros_per_day

    def quote(self, start: date, end: date) -> float:
        """Price in euros for a rental from start to end."""
        return self.euros_per_day * (end - start).days
