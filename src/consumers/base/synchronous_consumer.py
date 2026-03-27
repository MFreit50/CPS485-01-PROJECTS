import logging
from abc import abstractmethod

from src.core.contracts.consumer import Consumer
from src.core.contracts.event import Event

logger = logging.getLogger(__name__)


class SynchronousConsumer(Consumer):
    """
    A synchronous consumer that processes events in a blocking manner.
    """

    async def on_event(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer.
        Args:
            event (Event): The event to be handled
        """
        try:
            self._handle(event)
        except Exception:
            logger.exception(
                "SynchronousConsumer failed to process event",
                extra={"consumer": self.__class__.__name__, "event": event},
            )

    @abstractmethod
    def _handle(self, event: Event) -> None:
        """
        Internal method to handle the event. Subclasses should implement this method.
        Args:
            event (Event): The event to be handled
        """
        pass

    @property
    def consumer_id(self) -> str:
        """
        Unique identifier for the consumer, defaulting to the class name.
        Returns:
            str: The unique consumer ID
        """
        return self.__class__.__name__
