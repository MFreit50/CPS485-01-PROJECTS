from typing import Optional

from src.core.contracts.producer import Producer
from src.core.contracts.clock import Clock
from src.core.contracts.event import Event
from src.core.errors import InvalidLifecycleError

class FibonacciProducer(Producer):
    """
    Producer that emits Fibonacci numbers step by step.
    """

    def __init__(self, clock: Clock, max_count: int) -> None:
        """
        Args:
            clock (Clock): The clock instance to track steps.
            max_count (int): The maximum number of Fibonacci numbers to produce.
        """
        self._clock = clock
        self._max_count = max_count

        self._index = 0
        self.previous = 0
        self.current = 1

        self._started = False
        self._finished = False
    
    def start(self) -> None:
        """
        Initialize the Producer.
        Must be called before step().
        Raises:
            InvalidLifecycleError: if called more than once
        """
        
        if self._started:
            raise InvalidLifecycleError("Producer.start() called more than once.")
        
        self._started = True
        self._finished = False
    
    def step(self) -> Optional[Event]:
        """
        Execute a single step of the Fibonacci sequence.
        Returns:
            An Event if the current index is less than max_count,
            else None.
        Raises:
            InvalidLifecycleError: 
                - if step() is called before start()
                - if step() is called after completion
        """

        if not self._started:
            raise InvalidLifecycleError("Producer.step() called before start().")
        if self._finished:
            raise InvalidLifecycleError("Producer.step() called after completion.")

        if self._index >= self._max_count:
            self._finished = True
            return None
        
        #Generate the next Fibonacci number
        value = self.previous
        self.previous, self.current = (self.current, self.previous + self.current)

        event = Event(
            event_type="fibonacci_number",
            step=self._clock.now(),
            payload={"index": self._index, "value": value}
        )

        self._index += 1
        self._clock.tick()

        return event
    
    def is_finished(self) -> bool:
        """
        Check if the Producer has completed execution.
        Returns:
            True if finished, else False
        """
        return self._finished