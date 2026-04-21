from dataclasses import dataclass

from src.producers.nn.events.neuron_update_step_result import NeuronUpdateStepResult


@dataclass(frozen=True)
class LayerUpdateStepResult:
    layer_id: str
    neuron_result: NeuronUpdateStepResult
