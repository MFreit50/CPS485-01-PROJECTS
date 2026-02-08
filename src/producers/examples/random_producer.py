import random

from src.core.contracts.read_only_clock import ReadOnlyClock
from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event

class SeededRandomProducer(BaseProducer):
    """
    A producer that emits deterministic random numbers at each step.
    """

    def __init__(self, clock: ReadOnlyClock, limit: int, seed: int) -> None:
        """
        Args:
            clock (ReadOnlyClock): The read-only clock instance to track steps.
            limit (int): The total number of events to emit before completion.
            seed (int): The seed for the random number generator.
        """
        super().__init__(clock=clock)
        self._limit = limit
        self._random = random.Random(seed)

    def _on_start(self) -> None:
        self._index = 0

    def _step(self, step: int) -> Event:
        """
        Execute a single step of the random number producer.
        Returns:
            An Event with a random number if within total_steps
        Raises:
            InvalidLifecycleError: 
                - if step() is called before start()
                - if step() is called after completion
        """

        random_value = self._random.random()

        event = Event(
            event_type="random_number",
            step=step,
            payload={"value": random_value}
        )
        self._index += 1

        if self._index >= self._limit:
            self._finished = True

        return event