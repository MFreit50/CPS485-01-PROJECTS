from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class NeuronUpdateStepResult:
    neuron_id: str
    updated_weights: List[float]
    updated_bias: float
