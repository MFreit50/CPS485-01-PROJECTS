from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.time._read_only_clock_wrapper import _ReadOnlyClockWrapper
from src.core.contracts.clock import Clock
class SimpleClock(Clock):
    """
    A simple implementation of the Clock contract that tracks steps.
    """

    def __init__(self) -> None:
        self._time = 0

    def tick(self) -> int:
        """
        Increment the clock by one step and return the new step value.
        Returns:
            The current step after incrementing.
        """
        self._time += 1
        return self._time

    def now(self) -> int:
        """
        Get the current step without incrementing.
        Returns:
            The current step value.
        """
        return self._time
    
    def as_read_only(self) -> ReadOnlyClock:
        """
        Get a read-only view of this clock.
        Returns:
            A read-only wrapper around this clock instance.
        """
        return _ReadOnlyClockWrapper(self)