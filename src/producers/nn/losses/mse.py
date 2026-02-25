from typing import List
from src.producers.nn.losses.base import Loss

class MeanSquaredError(Loss):

    def compute(self, predicted: List[float], expected: List[float]) -> float:
        if len(predicted) != len(expected):
            raise ValueError("Predicted and expected outputs must have same length")
        
        weighted_sum: float = 0.0
        for p, e in zip(predicted, expected):
            weighted_sum += (p - e) ** 2

        loss: float = weighted_sum / len(predicted)
        return loss
    
    def derivative(self, predicted: List[float], expected: List[float]) -> List[float]:
        if len(predicted) != len(expected):
            raise ValueError("Predicted and expected outputs must have same length")
        
        n = len(predicted)
        return [2* (p - e) / n for p, e in zip(predicted, expected)]
    