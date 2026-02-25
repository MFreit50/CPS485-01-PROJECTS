from abc import ABC, abstractmethod

class Activation(ABC):
    """
    Base Class for activation functions
    """

    @abstractmethod
    def compute(self, z: float) -> float:
        pass

    @abstractmethod
    def derivative(self, a: float) -> float:
        pass