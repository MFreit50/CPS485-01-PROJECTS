from abc import ABC, abstractmethod

from .event import Event

class Producer(ABC):
    """
    Abstract base class for all event producers.

    - Producers generate events representing meaningful occurrences
    - Each producer has a unique identifier
    - Producers can emit events to be consumed by consumers

    """
    @property
    @abstractmethod
    def producer_id(self) -> str:
        """
        Unique identifier for the producer
        Returns:
            str: The unique producer ID
        """
        pass
    
    @abstractmethod
    def start(self) -> None:
        """
        Initialize algorithm state
        Must be called before step()

        Raises:
            InvalidLifecycleError: if called more than once
        """
        pass

    @abstractmethod
    def step(self, step: int) -> Event:
        """
        Execute a single step of the algorithm
        Args:
            step (int): The step number to execute
        Returns:
            An Event if a meaningful occurrence happened
            else None
        Raises:
            InvalidLifecycleError: if called before start()
            or after completion
        """
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        """
        Check if the algorithm has completed execution
        Returns:
            True if finished, else False
        """
        pass