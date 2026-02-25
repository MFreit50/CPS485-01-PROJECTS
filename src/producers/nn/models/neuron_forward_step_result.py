from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class NeuronForwardStepResult:
    neuron_id: str
    inputs: List[float]
    weights: List[float]
    bias: float
    z: float
    activation: float
