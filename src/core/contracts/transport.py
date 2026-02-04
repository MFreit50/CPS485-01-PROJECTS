from abc import ABC, abstractmethod
from .event import Event
from .consumer import Consumer

class Transport(ABC):
    """
    Abstract base class for all transport mechanisms

    - Responsible for moving events from producers to consumers
    
    """

    @abstractmethod
    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribed consumers.
        Args:
            event (Event): The event to be published
        """
        pass

    @abstractmethod
    def subscribe(self, consumer: Consumer) -> None:
        """
        Register a consumer to receive events.
        Args:
            consumer (Consumer): The consumer to subscribe
        """
        pass