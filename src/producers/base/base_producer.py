from abc import ABC, abstractmethod
from typing import Optional

from src.core.contracts.producer import Producer
from src.core.contracts.event import Event
from src.core.contracts.clock import Clock
from src.core.errors import InvalidLifecycleError

class BaseProducer(Producer, ABC):
    """
    Base implementation for all event producers.

    Enforces:
    - lifecycle correctness
    - clock availability
    """

    def __init__(self, *, clock: Clock) -> None:
        self._clock = clock

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
        self._on_start()

    def step(self) -> Optional[Event]:
        """
        Execute a single step of the producer.
        Returns:
            An Event if a meaningful occurrence happened,
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

        event = self._step()

        if self.is_finished():
            self._finished = True

        return event
    
    def is_finished(self) -> bool:
        """
        Returns True if the producer is finished.
        """
        return self._finished
    
    @property
    def clock(self) -> Clock:
        """
        Access the producer's clock.
        """
        return self._clock
    
    #Hooks for subclasses
    @abstractmethod
    def _step(self) -> Optional[Event]:
        """
        Internal step method to be implemented by subclasses.
        Returns:
            An Event if a meaningful occurrence happened,
            else None.
        """
        pass

    def _on_start(self) -> None:
        """
        Hook for subclasses to implement custom start logic.
        Called once when start() is invoked.
        """
        pass

