from abc import ABC, abstractmethod
from enum import Enum

from src.core.contracts.event import Event
from src.core.contracts.producer import Producer
from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.errors import InvalidLifecycleError
from src.core.id.identifiable import Identifiable


class ProducerState(Enum):
    INITIAL = 0
    RUNNING = 1
    FINISHED = 2


class BaseProducer(Producer, Identifiable, ABC):
    """
    Base implementation for all event producers.

    Enforces:
    - lifecycle correctness
    - clock availability
    """

    def __init__(self, *, clock: ReadOnlyClock) -> None:
        Producer.__init__(self)
        Identifiable.__init__(self)

        self._clock = clock
        self._state = ProducerState.INITIAL

    @property
    def producer_id(self) -> str:
        """
        Unique identifier for the producer
        Returns:
            str: The unique producer ID
        """
        return self.id

    def start(self) -> None:
        """
        Initialize the producer state.
        Must be called before step().
        Raises:
            InvalidLifecycleError: if called more than once
        """
        if self._state != ProducerState.INITIAL:
            raise InvalidLifecycleError("Producer.start() called more than once.")

        self._state = ProducerState.RUNNING
        self._on_start()

    def step(self, timestamp: int) -> Event:
        """
        Execute a single step of the producer.
        Args:
            timestamp (int): The logical clock time when the step occurred
        Returns:
            An Event if a meaningful occurrence happened,
            else None.
        Raises:
            InvalidLifecycleError:
                - if step() is called before start()
                - if step() is called after completion
        """

        if self._state != ProducerState.RUNNING:
            raise InvalidLifecycleError(
                "Producer.step() called before start() or after completion."
            )

        event: Event = self._step(timestamp)

        return event

    def _mark_finished(self) -> None:
        """
        Mark the producer as finished.
        Should be called by subclasses when they determine they are done.
        """
        self._state = ProducerState.FINISHED

    def is_finished(self) -> bool:
        """
        Returns True if the producer is finished.
        """
        return self._state == ProducerState.FINISHED

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

    # Hooks for subclasses
    @abstractmethod
    def _step(self, timestamp: int) -> Event:
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
