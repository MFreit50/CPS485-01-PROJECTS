from __future__ import annotations
from dataclasses import dataclass
from typing import List

from src.core.contracts.event import Event
from src.producers.nn.models.neuron_forward_step_result import NeuronForwardStepResult
from src.producers.nn.models.layer_forward_step_result import LayerForwardStepResult

@dataclass(frozen=True)
class ForwardPropagationStep(Event):
    """
    Emitted when a neuron is activated during the forward pass of training
    """
    epoch: int
    sample_index: int
    layer_id: str
    neuron_id: str
    inputs: List[float]
    weights: List[float]
    bias: float
    z: float
    activation: float

    @classmethod
    def from_forward_result(
        cls,
        *,
        timestamp: int,
        producer_id: str,
        epoch: int,
        sample_index: int,
        layer_result: LayerForwardStepResult
    ) -> ForwardPropagationStep:
        
        neuron_result : NeuronForwardStepResult= layer_result.neuron_result

        return cls(
            timestamp= timestamp,
            producer_id= producer_id,
            epoch = epoch,
            sample_index=sample_index,
            layer_id= layer_result.layer_id,
            neuron_id= neuron_result.neuron_id,
            inputs= neuron_result.inputs,
            weights= neuron_result.weights,
            bias= neuron_result.bias,
            z= neuron_result.z,
            activation= neuron_result.activation
        )