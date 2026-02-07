from typing import Optional, List

from src.core.contracts.runner import Runner
from src.core.contracts.clock import Clock
from src.core.contracts.runner_tracer import RunnerTracer
from src.core.contracts.producer import Producer
from src.core.contracts.transport import Transport
from src.core.errors import InvalidLifecycleError

class SimpleRunner(Runner):
    """
    A basic synchronous runner that executes producers step by step until completion.
    """

    def __init__(self, *, clock: Clock, producers:List[Producer], transport: Transport, tracer: Optional[RunnerTracer] = None) -> None:
        if not producers:
            raise InvalidLifecycleError("SimpleRunner requires at least one producer.")
        
        if len(set(producers)) != len(producers):
            raise InvalidLifecycleError("SimpleRunner received duplicate producers.")
        
        self._clock = clock
        self._producers: List[Producer] = list(producers)
        self._transport = transport
        self._tracer = tracer

        self._started = False
        self._finished = False

    def start(self) -> None:
        """
        Initialize the runner and all producers.
        Must be called before step().
        Raises:
            InvalidLifecycleError: if called more than once
        """
        if self._started:
            raise InvalidLifecycleError("SimpleRunner.start() called more than once.")
        
        self._started = True
        self._finished = False

        for producer in self._producers:
            producer.start()

    def step(self) -> None:
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

        if not self._started:
            raise InvalidLifecycleError("SimpleRunner.step() called before run().")
        if self._finished:
            raise InvalidLifecycleError("SimpleRunner.step() called after completion.")

        step = self._clock.tick()

        for producer in self._producers:
            if producer.is_finished():
                continue

            event = producer.step()
            if event is not None:
                self._transport.publish(event)
                if self._tracer:
                    self._tracer.record_step(producer_id=producer.producer_id, event=event, step=step)
        
        if self._all_finished():
            self._finished = True

    def run(self) -> None:
        """Run all producers until completion."""
        
        if not self._started:
            self.start()
        
        while not self.is_finished():
            self.step()

    def is_finished(self) -> bool:
        """
        Check if all producers have completed execution.
        Returns:
            True if all producers are finished, else False
        """
        return self._finished
    
    def _all_finished(self) -> bool:
        """Check if all producers have finished."""
        return all(producer.is_finished() for producer in self._producers)