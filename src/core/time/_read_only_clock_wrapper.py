from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.contracts.clock import Clock

class _ReadOnlyClockWrapper(ReadOnlyClock):
    def __init__(self, clock : Clock) -> None:
        """
        A wrapper around a Clock instance that provides read-only access to the current time.
        """
        self._clock = clock

    def now(self) -> int:
        return self._clock.now()