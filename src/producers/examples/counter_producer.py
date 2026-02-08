from src.core.contracts.read_only_clock import ReadOnlyClock
from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event

class CounterProducer(BaseProducer):
    """
    A simple producer that counts from 0 to a limit,
    emitting an event at each step.
    """

    def __init__(self, *, clock : ReadOnlyClock, limit: int) -> None:
        """
        Args:
            clock (ReadOnlyClock): The read-only clock instance to track steps.
            limit (int): The total number of events to emit before completion.
        """
        super().__init__(clock=clock)
        self._limit = limit

    def _on_start(self) -> None:
        self._index = 0
    
    def _step(self, step: int) -> Event:
        """
        Execute a single counting step.
        Returns:
            An Event if the current value is less than limit
        Raises:
            InvalidLifecycleError:
                -if step() is called before start()
                -if step() is called after completion
        """

        event = Event(
            event_type="counter_increment",
            step=step,
            payload={"value": self._index}
        )

        self._index += 1

        if self._index >= self._limit:
            self._finished = True
        
        return event