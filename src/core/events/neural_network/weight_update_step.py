from __future__ import annotations
from dataclasses import dataclass
from typing import List

from src.core.contracts.event import Event
from src.producers.nn.models.layer_update_step_result import LayerUpdateStepResult
from src.producers.nn.models.neuron_update_step_result import NeuronUpdateStepResult

@dataclass(frozen=True)
class WeightUpdateStep(Event):
    """
    Emitted when a neuron's weight and bias is tweaked after backward propagation
    """
    epoch: int
    sample_index: int
    layer_id: str
    neuron_id: str
    updated_weights: List[float]
    updated_bias: float
    

    @classmethod
    def from_update_result(
        cls,
        *,
        timestamp: int,
        producer_id: str,
        epoch: int,
        sample_index: int,
        layer_result: LayerUpdateStepResult
    ) -> WeightUpdateStep:
        
        neuron_result : NeuronUpdateStepResult= layer_result.neuron_result

        return cls(
            timestamp= timestamp,
            producer_id= producer_id,
            epoch = epoch,
            sample_index=sample_index,
            layer_id= layer_result.layer_id,
            neuron_id= neuron_result.neuron_id,
            updated_weights=neuron_result.updated_weights,
            updated_bias=neuron_result.updated_bias
        )