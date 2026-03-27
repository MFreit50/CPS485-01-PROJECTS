from typing import Optional

from src.core.contracts.clock import Clock
from src.core.contracts.runner_tracer import RunnerTracer
from src.core.contracts.transport import Transport
from src.core.execution.base.base_runner import BaseRunner


class SimpleRunner(BaseRunner):
    """
    SimpleRunner is a straightforward implementation
    of the Runner interface that executes producers
    sequentially in a single thread.
    """

    def __init__(
        self,
        *,
        clock: Clock,
        transport: Transport,
        tracer: Optional[RunnerTracer] = None
    ) -> None:
        super().__init__(clock=clock, transport=transport, tracer=tracer)
