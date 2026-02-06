from typing import Optional, List
from src.core.contracts.transport import Transport
from src.core.contracts.consumer import Consumer
from src.core.contracts.event import Event
from src.core.errors import InvalidEventError

class InMemoryTransport(Transport):
    """
    In-memory transport mechanism for moving events from producers to consumers.

    - Stores events in memory
    - Delivers events to all subscribed consumers immediately upon publishing

    """

    def __init__(self, consumers: Optional[List[Consumer]] = None) -> None:
        """
        Initialize the transporter.

        Args:
            consumers (Optional[List[Consumer]]): List of Consumer objects. If None, an empty list is created.
        """
        self.consumers: List[Consumer] = consumers if consumers is not None else []

    def subscribe(self, consumer: Consumer) -> None:
        """
        Register a consumer to receive events.
        Args:
            consumer (Consumer): The consumer to subscribe
        """
        self.consumers.append(consumer)

    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribed consumers.
        Args:
            event (Event): The event to be published
        Raises:
            InvalidEventError: if the event is invalid.
        """

        if event is None:
            raise InvalidEventError("Cannot publish a None event.")
        
        for consumer in self.consumers:
            consumer.on_event(event)
