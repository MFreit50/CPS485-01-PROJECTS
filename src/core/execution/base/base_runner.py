from enum import Enum
from typing import List, Optional

from src.core.contracts.clock import Clock
from src.core.contracts.event import Event
from src.core.contracts.producer import Producer
from src.core.contracts.runner import Runner
from src.core.contracts.runner_tracer import RunnerTracer
from src.core.contracts.transport import Transport
from src.core.errors import InvalidLifecycleError
from src.core.id.identifiable import Identifiable


class RunnerState(Enum):
    INITIAL = 0
    RUNNING = 1
    FINISHED = 2


class BaseRunner(Runner, Identifiable):
    """
    BaseRunner provides a common implementation for Runner interface.
    It manages the lifecycle and execution flow of producers.
    Subclasses can override specific methods to customize behavior.
    """

    def __init__(
        self,
        *,
        clock: Clock,
        transport: Transport,
        tracer: Optional[RunnerTracer] = None
    ) -> None:
        Identifiable.__init__(self)

        self._clock: Clock = clock
        self._transport: Transport = transport
        self._tracer: Optional[RunnerTracer] = tracer

        self._producers: List[Producer] = []
        self._state: RunnerState = RunnerState.INITIAL
        self._timestamp = 0

    def add_producer(self, producer: Producer) -> None:
        """
        Add a producer to the runner.
        Must be called before start().
        Raises:
            InvalidLifecycleError: if called after start()
            InvalidLifecycleError: if producer is already added
        """
        if self._state != RunnerState.INITIAL:
            raise InvalidLifecycleError(
                "Cannot add producers after the runner has started."
            )

        if producer in self._producers:
            raise InvalidLifecycleError("Producer is already added to the runner.")

        self._producers.append(producer)

    async def start(self) -> None:
        """
        Initialize the runner and all producers.
        Must be called before step().
        Raises:
            InvalidLifecycleError: if called more than once
        """
        if self._state != RunnerState.INITIAL:
            raise InvalidLifecycleError("Runner.start() called more than once.")

        self._validate_producers()
        self._state = RunnerState.RUNNING
        self._timestamp = 0

        for producer in self._producers:
            producer.start()

        await self._transport.start()

    async def step(self) -> None:
        """
        Execute a single step for all producers.

        One step involves:
        - ticking the clock
        - stepping each active producer
        - publishing any generated events

        Raises:
            InvalidLifecycleError:
                - if step() is called before run()
                - if step() is called after completion
        """

        if self._state != RunnerState.RUNNING:
            raise InvalidLifecycleError(
                "Runner.step() called before run() or after completion."
            )

        for producer in self._producers:
            if producer.is_finished():
                continue

            event: Event = producer.step(self._timestamp)

            if event is not None:
                await self._transport.publish(event)
                if self._tracer:
                    self._tracer.record_step(
                        producer_id=producer.producer_id,
                        event=event,
                        timestamp=self._timestamp,
                    )

            self._timestamp = self._clock.tick()

        if self._all_finished():
            self._mark_finished()

    async def run(self) -> None:
        """Run all producers until completion."""

        if self._state == RunnerState.INITIAL:
            await self.start()

        while not self.is_finished():
            await self.step()

    def is_finished(self) -> bool:
        """
        Check if all producers have completed execution.
        Returns:
            True if all producers are finished, else False
        """
        return self._state == RunnerState.FINISHED

    @property
    def runner_id(self) -> str:
        """
        Unique identifier for the runner instance.
        Returns:
            str: The unique runner ID
        """
        return self.id

    def _mark_finished(self) -> None:
        self._state = RunnerState.FINISHED

    def _all_finished(self) -> bool:
        """Check if all producers have finished."""
        return all(producer.is_finished() for producer in self._producers)

    def _validate_producers(self) -> None:
        """
        Validate the list of producers before starting execution.
        Raises:
            InvalidLifecycleError: if no producers are provided
            InvalidLifecycleError: if duplicate producers are detected
        """

        if not self._producers:
            raise InvalidLifecycleError("Runner requires at least one producer.")

        if len(set(self._producers)) != len(self._producers):
            raise InvalidLifecycleError("Runner received duplicate producers.")
