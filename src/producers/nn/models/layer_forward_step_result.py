from dataclasses import dataclass

from src.producers.nn.models.neuron_forward_step_result import NeuronForwardStepResult

@dataclass(frozen=True)
class LayerForwardStepResult:
    layer_id: str
    neuron_result: NeuronForwardStepResult
