import logging
from abc import abstractmethod

from src.consumers.base.base_consumer import BaseConsumer
from src.core.contracts.event import Event

logger = logging.getLogger(__name__)


class AsynchronousConsumer(BaseConsumer):
    """
    An asynchronous consumer that processes events in a non-blocking manner.
    """

    async def on_event(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer asynchronously.
        Args:
            event (Event): The event to be handled
        """
        try:
            await self._handle(event)
        except Exception:
            logger.exception(
                "AsynchronousConsumer failed to process event",
                extra={"consumer": self.__class__.__name__, "event": event},
            )

    @abstractmethod
    async def _handle(self, event: Event) -> None:
        """
        Internal method to handle the event. Subclasses should implement this method.
        Args:
            event (Event): The event to be handled
        """
        pass
