from dataclasses import dataclass
from src.core.contracts.event import Event

@dataclass(frozen=True)
class TrainingComplete(Event):
    """
    Emitted when training is complete for a neural network.
    """
    
    final_loss: float