import threading

from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.contracts.clock import Clock

class _ThreadSafeReadOnlyClockWrapper(ReadOnlyClock):
    def __init__(self, clock : Clock) -> None:
        """
        A wrapper around a Clock instance that provides read-only access to the current time.
        """
        self._clock = clock
        self._lock = threading.Lock()

    def now(self) -> int:
        with self._lock:
            return self._clock.now()