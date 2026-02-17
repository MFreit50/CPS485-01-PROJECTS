import threading

from core.time._thread_safe_read_only_clock_wrapper import _ThreadSafeReadOnlyClockWrapper
from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.contracts.clock import Clock

class ThreadSafeClock(Clock):
    """
    A thread-safe implementation of the Clock contract that tracks steps.
    """

    def __init__(self) -> None:
        self._time = 0
        self._lock = threading.Lock()

    def tick(self) -> int:
        """
        Increment the clock by one step and return the new step value.
        Returns:
            The current step after incrementing.
        """
        with self._lock:
            self._time += 1
            return self._time

    def now(self) -> int:
        """
        Get the current step without incrementing.
        Returns:
            The current step value.
        """
        with self._lock:
            return self._time
    
    def as_read_only(self) -> ReadOnlyClock:
        """
        Get a thread-safe read-only view of this clock.
        Returns:
            A thread-safe read-only wrapper around this clock instance.
        """
        return _ThreadSafeReadOnlyClockWrapper(self)