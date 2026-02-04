from abc import ABC, abstractmethod
from .event import Event

class Consumer(ABC):
    """
    Abstract base class for all event consumers

    - Consumers process events emitted by producers
    - Each consumer has a unique identifier
    - Consumers interpret events to perform actions (e.g., visualization, logging)

    """

    @abstractmethod
    def on_event(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer.
        Args:
            event (Event): The event to be handled
        """
        pass