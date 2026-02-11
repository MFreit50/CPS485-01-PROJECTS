from src.core.contracts.read_only_clock import ReadOnlyClock
from src.producers.base.base_producer import BaseProducer
from src.core.events.counter.counter_number import CounterNumber

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
    
    def _step(self, timestamp: int) -> CounterNumber:
        """
        Execute a single counting step.
        Args:
            timestamp (int): The logical clock time when the step occurred
        Returns:
            A CounterNumber event if the current value is less than limit
        Raises:
            InvalidLifecycleError:
                -if step() is called before start()
                -if step() is called after completion
        """

        event = CounterNumber(
            timestamp=timestamp,
            producer_id=self._producer_id,
            value=self._index
        )

        self._index += 1

        if self._index >= self._limit:
            self._finished = True
        
        return event