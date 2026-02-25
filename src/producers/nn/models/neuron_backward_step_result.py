from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class NeuronBackwardStepResult:
    neuron_id: str
    grad_output: float
    delta: float
    grad_z: float
    grad_weights: List[float]
    grad_inputs: List[float]
    grad_bias: float