import random
from typing import Optional

from src.producers.base.base_producer import BaseProducer
from src.core.contracts.clock import Clock
from src.core.contracts.event import Event

class SeededRandomProducer(BaseProducer):
    """
    A producer that emits deterministic random numbers at each step.
    """

    def __init__(self, clock: Clock, limit: int, seed: int) -> None:
        """
        Args:
            clock (Clock): The clock instance to track steps.
            limit (int): The total number of steps to produce events for.
            seed (int): The seed for the random number generator.
        """
        super().__init__(clock=clock)
        self._limit = limit
        self._random = random.Random(seed)

    def _on_start(self) -> None:
        self._index = 0

    def _step(self) -> Optional[Event]:
        """
        Execute a single step of the random number producer.
        Returns:
            An Event with a random number if within total_steps,
            else None.
        Raises:
            InvalidLifecycleError: 
                - if step() is called before start()
                - if step() is called after completion
        """
        if self._index >= self._limit:
            self._finished = True
            return None
        
        step = self._clock.tick()

        random_value = self._random.random()

        event = Event(
            event_type="random_number",
            step=step,
            payload={"value": random_value}
        )
        self._index += 1
        return event