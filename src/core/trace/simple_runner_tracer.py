from typing import List

from src.core.contracts.runner_tracer import RunnerTracer
from src.core.contracts.trace_entry import TraceEntry
from src.core.contracts.event import Event

class SimpleRunnerTracer(RunnerTracer):
    """
    Simple implementation of RunnerTracer that stores trace entries in memory.
    Responsibilities:
    - Record each step of the execution with associated events
    - Provide access to the complete trace log for analysis
    """

    def __init__(self) -> None:
        self._trace_log: List[TraceEntry] = []

    def record_step(self, producer_id: str, timestamp: int, event: Event) -> None:
        """
        Record a single step in the execution trace.
        Args:
            producer_id (str): The unique identifier of the producer that executed the step
            timestamp (int): The logical clock time when the step occurred
            event (Event): The event emitted by the producer during this step
        """
        entry = TraceEntry(event=event, producer_id=producer_id, timestamp=timestamp)
        self._trace_log.append(entry)
    
    def get_trace(self) -> List[TraceEntry]:
        """
        Get the copy of the trace log generated so far.
        Returns:
            A list of TraceEntry objects representing the execution trace.
        """
        return self._trace_log.copy()