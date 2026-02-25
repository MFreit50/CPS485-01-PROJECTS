from enum import Enum

class NN_State(Enum):
    FORWARD_PROPAGATION = "forward_propagation"
    COMPUTE_LOSS = "loss"
    BACKWARD_PROPAGATION = "backwards_propagation"
    WEIGHT_UPDATE = "weight_update"
