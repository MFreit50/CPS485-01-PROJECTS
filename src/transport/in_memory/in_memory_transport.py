import queue
import threading
from typing import List

from src.core.contracts.event import Event
from src.transport.base.base_transport import BaseTransport


class InMemoryTransport(BaseTransport):
    """
    In-memory transport mechanism for moving events from producers to consumers asynchronously.
    - Delivers events to consumers using a thread pool and an internal queue.
    """

    def __init__(self, number_of_workers: int = 1) -> None:
        super().__init__()

        self.number_of_workers = number_of_workers
        self._queue: queue.Queue[Event] = queue.Queue()
        self._workers: List[threading.Thread] = []
        self._stop_event = threading.Event()

        self._start_workers()

    def _start_workers(self) -> None:
        """
        Start worker threads to process events from the queue.
        """
        for i in range(self.number_of_workers):
            worker = threading.Thread(
                target=self._worker_loop, name=f"InMemoryWorker-{i}", daemon=True
            )
            worker.start()
            self._workers.append(worker)

    def _worker_loop(self) -> None:
        """
        Worker thread loop to process events from the queue and publish them to consumers.
        """
        while not self._stop_event.is_set():
            try:
                event: Event = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            self._dispatch_event(event)
            self._queue.task_done()

    def publish(self, event: Event) -> None:
        """
        Adds an event to the internal queue to be processed by worker threads.
        Args:
            event (Event): The event to be published
        Raises:
            InvalidEventError: if the event is invalid.
            InvalidLifecycleError: if there are no consumers subscribed.
        """

        self._validate_event(event)
        self._queue.put(event)

    def flush(self) -> None:
        """
        Wait until all events in the queue have been processed.
        """
        self._queue.join()

    def shutdown(self) -> None:
        """
        Stop all worker threads gracefully.
        """
        self._stop_event.set()
        for worker in self._workers:
            worker.join()
