from dataclasses import dataclass
from typing import List

from src.core.contracts.event import Event

@dataclass(frozen=True)
class LossComputed(Event):
    """
    Emitted when the loss is computed for a training sample.
    """
    
    epoch: int
    sample_index: int
    predicted: List[float]
    expected: List[float]
    loss: float
    grad_inputs: List[float]