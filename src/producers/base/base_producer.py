from abc import ABC, abstractmethod
from typing import ClassVar, Optional

from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.contracts.producer import Producer
from src.core.contracts.event import Event
from src.core.errors import InvalidLifecycleError

class BaseProducer(Producer, ABC):
    """
    Base implementation for all event producers.

    Enforces:
    - lifecycle correctness
    - clock availability
    """

    _counter: ClassVar[int] = 0
    
    def __init__(self, *, clock: ReadOnlyClock) -> None:
        self._clock = clock

        self._started = False
        self._finished = False

        self._producer_id = f"{self.__class__.__name__}_{BaseProducer._counter}"
        BaseProducer._counter += 1

    @property
    def producer_id(self) -> str:
        """
        Unique identifier for the producer instance.
        """
        return self._producer_id
    
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

    def step(self, step: int) -> Event:
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

        event = self._step(step)

        if self.is_finished():
            self._finished = True

        return event
    
    def is_finished(self) -> bool:
        """
        Returns True if the producer is finished.
        """
        return self._finished

    @property
    def clock(self) -> ReadOnlyClock:
        """
        Access the producer's clock instance.
        Returns:
            The clock instance provided at initialization.
        Note:
            This is a read-only view of the clock to prevent producers
            from modifying time directly.
        """
        return self._clock
    
    @property
    def now(self) -> int:
        """
        Get the current time from the clock.
        Returns:
            The current time as an integer step count.
        """
        return self._clock.now()
    
    #Hooks for subclasses
    @abstractmethod
    def _step(self, step: int) -> Event:
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

