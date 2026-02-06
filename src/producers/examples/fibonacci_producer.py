from typing import Optional

from src.producers.base.base_producer import BaseProducer
from src.core.contracts.clock import Clock
from src.core.contracts.event import Event

class FibonacciProducer(BaseProducer):
    """
    Producer that emits Fibonacci numbers step by step.
    """

    def __init__(self, clock: Clock, limit: int) -> None:
        """
        Args:
            clock (Clock): The clock instance to track steps.
            limit (int): The maximum number of Fibonacci numbers to produce.
        """
        super().__init__(clock=clock)
        self._limit = limit

    def _on_start(self) -> None:
        self.previous = 0
        self.current = 1
        self._index = 0

    def _step(self) -> Optional[Event]:
        """
        Execute a single step to produce the next Fibonacci number.
        Returns:
            An Event with the next Fibonacci number if within limit,
            else None.
        Raises:
            InvalidLifecycleError:
                -if step() is called before start()
                -if step() is called after completion
        """

        if self._index >= self._limit:
            self._finished = True
            return None
        
        step = self._clock.tick()

        event = Event(
            event_type="fibonacci_number",
            step=step,
            payload={"index": self._index, "value": self.previous}
        )
        # Generate the next Fibonacci number
        self.previous, self.current = (self.current, self.previous + self.current)

        self._index += 1

        return event
