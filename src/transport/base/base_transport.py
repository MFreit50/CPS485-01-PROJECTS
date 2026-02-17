from abc import ABC, abstractmethod
from typing import List

from src.core.contracts.event import Event
from src.core.contracts.transport import Transport
from src.core.contracts.consumer import Consumer
from src.core.errors import InvalidEventError, InvalidLifecycleError

class BaseTransport(Transport, ABC):
    """
    Base implementation for all transport mechanisms.

    Responsibilites:
    - Manage consumer subscriptions
    - Centralize event distribution to consumers
    - Provide lifecycle management
    """

    def __init__(self) -> None:
        self._consumers: List[Consumer] = []

    def subscribe(self, consumer: Consumer) -> None:
        if consumer in self._consumers:
            raise InvalidLifecycleError("Consumer is already subscribed.")
        self._consumers.append(consumer)
    
    def unsubscribe(self, consumer: Consumer) -> None:
        try:
            self._consumers.remove(consumer)
        except ValueError:
            raise InvalidLifecycleError("Consumer is not subscribed.")
    
    @property
    def consumers(self) -> List[Consumer]:
        """Read-only access to the list of subscribed consumers."""
        return self._consumers.copy()
    
    def publish(self, event: Event) -> None:
        if not isinstance(event, Event):
            raise InvalidEventError("Invalid event type.")
        if not self._consumers:
            raise InvalidLifecycleError("No consumers subscribed to receive events.")
        
        for consumer in self._consumers:
            consumer.on_event(event)