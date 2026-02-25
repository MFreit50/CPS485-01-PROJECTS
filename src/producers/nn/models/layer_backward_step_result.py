from dataclasses import dataclass

from src.producers.nn.models.neuron_backward_step_result import NeuronBackwardStepResult

@dataclass(frozen=True)
class LayerBackwardStepResult:
    layer_id: str
    neuron_result: NeuronBackwardStepResult
