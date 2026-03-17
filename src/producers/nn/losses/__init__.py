from src.producers.nn.losses.bce import BinaryCrossEntropy
from src.producers.nn.losses.mse import MeanSquaredError
from src.producers.nn.losses.registry import LossRegistry

LossRegistry.register("mse", MeanSquaredError)
LossRegistry.register("bce", BinaryCrossEntropy)
