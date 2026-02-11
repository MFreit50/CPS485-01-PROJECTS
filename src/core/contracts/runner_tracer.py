from abc import ABC, abstractmethod
from typing import List

from src.core.contracts.trace_entry import TraceEntry
from src.core.contracts.event import Event

class RunnerTracer(ABC):
    """
        Contract for recording the execution trace of a Runner.
        Responsibilities:
        - Record each timestamp of the execution with associated events
        - Provide access to the complete trace log for analysis
    """

    @abstractmethod
    def record_step(self, producer_id: str, timestamp: int, event: Event) -> None:
        """
        Record a single step in the execution trace.
        Args:
            producer_id (str): The unique identifier of the producer that executed the step
            timestamp (int): The logical clock time when the step occurred
            event (Event): The event emitted by the producer during this step
        """
        pass

    @abstractmethod
    def get_trace(self) -> List[TraceEntry]:
        """
        Get the copy of the trace log generated so far.
        Returns:
            A list of TraceEntry objects representing the execution trace.
        """
        pass