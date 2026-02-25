from __future__ import annotations
from dataclasses import dataclass
from typing import List

from src.core.contracts.event import Event
from src.producers.nn.models.layer_backward_step_result import LayerBackwardStepResult
from src.producers.nn.models.neuron_backward_step_result import NeuronBackwardStepResult

@dataclass(frozen=True)
class BackwardPropagationStep(Event):
    """
    Emitted when a step of backwards propagation is completed
    """
    
    epoch: int
    sample_index: int
    layer_id: str
    neuron_id: str
    grad_output: float
    delta: float
    grad_z: float
    grad_weights: List[float]
    grad_inputs: List[float]
    grad_bias: float

    @classmethod
    def from_backward_result(
        cls,
        *,
        timestamp: int,
        producer_id: str,
        epoch: int,
        sample_index: int,
        layer_result: LayerBackwardStepResult
    ) -> BackwardPropagationStep:
        
        neuron_result : NeuronBackwardStepResult= layer_result.neuron_result

        return cls(
            timestamp=timestamp,
            producer_id=producer_id,
            epoch=epoch,
            sample_index=sample_index,
            layer_id=layer_result.layer_id,
            neuron_id=neuron_result.neuron_id,
            grad_output=neuron_result.grad_output,
            delta=neuron_result.delta,
            grad_z=neuron_result.grad_z,
            grad_weights=neuron_result.grad_weights,
            grad_inputs=neuron_result.grad_inputs,
            grad_bias=neuron_result.grad_bias
        )