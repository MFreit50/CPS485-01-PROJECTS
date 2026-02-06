from typing import Optional
from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event
from src.core.contracts.clock import Clock

class CounterProducer(BaseProducer):
    """
    A simple producer that counts from 0 to a limit,
    emitting an event at each step.
    """

    def __init__(self, *, clock : Clock, limit: int) -> None:
        """
        Args:
            clock (Clock): The clock instance to track steps.
            limit (int): The maximum count value.
        """
        super().__init__(clock=clock)
        self._limit = limit

    def _on_start(self) -> None:
        self._index = 0
    
    def _step(self) -> Optional[Event]:
        """
        Execute a single counting step.
        Returns:
            An Event if the current value is less than limit,
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
            event_type="counter_increment",
            step=step,
            payload={"value": self._index}
        )

        self._index += 1
        
        return event