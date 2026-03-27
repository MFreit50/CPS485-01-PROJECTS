import asyncio
import logging
from typing import List

from src.core.contracts.event import Event
from src.transport.base.base_transport import BaseTransport, TransportState
from src.transport.sentinel_stop_signal import SentinelStopSignal

_STOP = SentinelStopSignal()
logger = logging.getLogger(__name__)


class InMemoryTransport(BaseTransport):
    """
    In-memory transport mechanism for moving events from producers to consumers asynchronously.
    - Delivers events to subscribed consumers using an internal asyncio queue and worker tasks.
    """

    def __init__(self, number_of_workers: int = 1) -> None:
        super().__init__()

        self._number_of_workers = number_of_workers
        self._queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=10000)
        self._tasks: List[asyncio.Task] = []

    async def start(self) -> None:
        """
        Start worker tasks to process events from the queue.
        """
        await super().start()
        for i in range(self._number_of_workers):
            task = asyncio.create_task(
                self._worker_loop(worker_id=i), name=f"InMemoryWorker-{i}"
            )
            self._tasks.append(task)

    async def _worker_loop(self, worker_id: int) -> None:
        """
        Worker task loop to process events from the queue and publish them to consumers.
        """
        while True:
            event: Event = await self._queue.get()

            if event is _STOP:
                self._queue.task_done()
                logger.debug(
                    "Worker received stop signal, exiting.",
                    extra={"worker_id": worker_id},
                )
                return

            try:
                await self._dispatch_event(event)
            except Exception as e:
                logger.error(
                    f"Error occurred while dispatching event: {e}",
                    extra={"worker_id": worker_id, "event": event},
                )
            finally:
                self._queue.task_done()

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
        await self._queue.put(event)

    async def flush(self) -> None:
        """
        Wait until all events in the queue have been processed.
        """
        await self._queue.join()

    async def shutdown(self) -> None:
        """
        Stop all worker tasks gracefully.
        """
        await super().shutdown()
        await self.flush()
        for _ in range(self._number_of_workers):
            await self._queue.put(_STOP)

        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        self._state = TransportState.FINISHED
