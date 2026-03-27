import logging
from abc import abstractmethod

from src.consumers.base.base_consumer import BaseConsumer
from src.core.contracts.event import Event

logger = logging.getLogger(__name__)


class SynchronousConsumer(BaseConsumer):
    """
    A synchronous consumer that processes events in a blocking manner.
    """

    def __init__(self):
        super().__init__()

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
