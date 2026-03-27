from abc import abstractmethod

from src.core.contracts.consumer import Consumer
from src.core.contracts.event import Event
from src.core.id.identifiable import Identifiable


class BaseConsumer(Consumer, Identifiable):
    """
    Base consumer class that all consumers should inherit from.
    Provides common functionality and enforces the implementation of the on_event method.
    """

    def __init__(self):
        Consumer.__init__(self)
        Identifiable.__init__(self)

    @property
    def consumer_id(self) -> str:
        """
        Unique identifier for the consumer
        Returns:
            str: The unique consumer ID
        """
        return self.id

    @abstractmethod
    async def on_event(self, event: Event) -> None:
        """
        Handle an incoming event. Must be implemented by subclasses.
        Args:
            event (Event): The event to handle
        """
        pass
