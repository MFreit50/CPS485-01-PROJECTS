from typing import Optional
from src.core.contracts.producer import Producer
from src.core.contracts.event import Event
from src.core.contracts.clock import Clock
from src.core.errors import InvalidLifecycleError

class CounterProducer(Producer):
    """
    A simple producer that counts from 0 to a max_value,
    emitting an event at each step.

    Args:
        max_value (int): The maximum count value.
        clock (Clock): The clock instance to track steps.
    """

    def __init__(self, clock : Clock, max_value: int) -> None:
        self._clock = clock
        self._max_value = max_value
        self._current = 0
        self._started = False
        self._finished = False

    def start(self) -> None:
        """
        Initialize the counter state.
        Must be called before step().
        """
        self._current = 0
        self._finished = False
        self._started = True

    def step(self) -> Optional[Event]:
        """
        Execute a single step of the counter.
        Returns:
            An Event if the current count is less than the max_value,
            else None.
        """

        if not self._started:
            raise InvalidLifecycleError("Producer.step() called before start().")
        if self._finished:
            raise InvalidLifecycleError("Producer.step() called after completion.")

        step = self._clock.tick()

        event = Event(
            event_type="counter_increment",
            step=step,
            payload={"value": self._current}
        )

        self._current += 1
        
        if self._current > self.max_value:
            self._finished = True
        
        return event

    def is_finished(self) -> bool:
        """
        Check if the counter has completed counting to the limit.
        Returns:
            True if finished, else False.
        """
        return self._finished