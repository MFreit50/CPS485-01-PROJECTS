import random

from src.core.contracts.read_only_clock import ReadOnlyClock
from src.producers.base.base_producer import BaseProducer
from src.core.events.counter.random_number_generator import RandomNumber

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

    def _step(self, timestamp: int) -> RandomNumber:
        """
        Execute a single step of the random number producer.
        Args:
            timestamp (int): The logical clock time when the step occurred
        Returns:
            An RandomNumber event with a random number if within total_steps
        Raises:
            InvalidLifecycleError: 
                - if step() is called before start()
                - if step() is called after completion
        """

        random_value = self._random.random()

        event = RandomNumber(
            timestamp=timestamp,
            producer_id=self._producer_id,
            value=random_value
        )
        self._index += 1

        if self._index >= self._limit:
            self._finished = True

        return event