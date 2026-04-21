import asyncio
import logging
from abc import ABC
from enum import Enum
from typing import List

from src.core.contracts.consumer import Consumer
from src.core.contracts.event import Event
from src.core.contracts.transport import Transport
from src.core.errors import InvalidEventError, InvalidLifecycleError

logger = logging.getLogger(__name__)


class TransportState(Enum):
    INITIAL = 0
    RUNNING = 1
    SHUTTING_DOWN = 2
    FINISHED = 3


class BaseTransport(Transport, ABC):
    """
    Base implementation for all transport mechanisms.

    Responsibilites:
    - Manage consumer subscriptions
    - Centralize event distribution to consumers
    - Provide lifecycle management
    """

    # TODO: Allow Consumers to subscribe to specific event types or producers in the future for more efficient routing

    def __init__(self) -> None:
        self._consumers: List[Consumer] = []
        self._state = TransportState.INITIAL

    async def start(self) -> None:
        """
        Base start method. Can be overridden by subclasses if needed.
        """
        if self._state != TransportState.INITIAL:
            raise InvalidLifecycleError("Transport has already been started.")

        self._state = TransportState.RUNNING

    async def shutdown(self) -> None:
        if self._state != TransportState.RUNNING:
            raise InvalidLifecycleError("Transport is not running.")

        self._state = TransportState.SHUTTING_DOWN

    def subscribe(self, consumer: Consumer) -> None:
        if consumer in self._consumers:
            raise InvalidLifecycleError("Consumer is already subscribed.")
        self._consumers.append(consumer)

    def unsubscribe(self, consumer: Consumer) -> None:
        try:
            self._consumers.remove(consumer)
        except ValueError:
            raise InvalidLifecycleError("Consumer is not subscribed.")

    async def publish(self, event: Event) -> None:
        """
        Adds an event to the internal queue to be processed by worker threads.
        Args:
            event (Event): The event to be published
        Raises:
            InvalidEventError: if the event is invalid.
            InvalidLifecycleError: if there are no consumers subscribed.
        """

        self._validate_transport_request(event)
        await self._dispatch_event(event)

    def _validate_transport_request(self, event: Event) -> None:
        """Validate the event before publishing."""
        if self._state != TransportState.RUNNING:
            raise InvalidLifecycleError("Transport is not running.")
        if not isinstance(event, Event):
            raise InvalidEventError("Invalid event type.")
        if not self._consumers:
            raise InvalidLifecycleError("No consumers subscribed to receive events.")

    async def _dispatch_event(self, event: Event) -> None:
        """Internal method to dispatch an event to all consumers."""
        results = await asyncio.gather(
            *(consumer.on_event(event) for consumer in self._consumers),
            return_exceptions=True,
        )

        for consumer, result in zip(self._consumers, results):
            if isinstance(result, Exception):
                logger.exception(
                    "Consumer raised an unhandled exception. This is a bug",
                    exc_info=result,
                    extra={
                        "consumer": consumer.__class__.__name__,
                        "event_type": event.__class__.__name__,
                    },
                )

    @property
    def consumers(self) -> List[Consumer]:
        """Read-only access to the list of subscribed consumers."""
        return self._consumers.copy()
