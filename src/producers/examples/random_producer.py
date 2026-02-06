import random
from typing import Optional

from src.core.contracts.producer import Producer
from src.core.contracts.clock import Clock
from src.core.contracts.event import Event
from src.core.errors import InvalidLifecycleError

class SeededRandomProducer(Producer):
    """
    A producer that emits deterministic random numbers at each step.
    """

    def __init__(self, clock: Clock, total_steps: int, seed: int) -> None:
        """
        Args:
            clock (Clock): The clock instance to track steps.
            total_steps (int): The total number of steps to produce events for.
            seed (int): The seed for the random number generator.
        """
        self._clock = clock
        self._total_steps = total_steps
        self._random = random.Random(seed)
        self._current_step = 0

        self._started = False
        self._finished = False
        

    def start(self) -> None:
        """
        Initialize the producer state.
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
        Execute a single step of the random number producer.
        Returns:
            An Event with a random number if within total_steps,
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

        if self._current_step >= self._total_steps:
            self._finished = True
            return None
        
        random_value = self._random.random()

        event = Event(
            event_type="random_number",
            step=self._clock.now(),
            payload={"value": random_value}
        )
        self._current_step += 1
        self._clock.tick()
        return event

    def is_finished(self) -> bool:
        """
        Check if the producer has completed execution.
        Returns:
            True if finished, else False
        """
        return self._finished