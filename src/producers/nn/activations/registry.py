from typing import Dict, Type

from src.producers.nn.activations.base import Activation


class ActivationRegistry:
    _registry: Dict[str, Type[Activation]] = {}

    @classmethod
    def register(cls, name: str, activation_cls: Type[Activation]) -> None:
        cls._registry[name.lower()] = activation_cls

    @classmethod
    def get(cls, name: str) -> Type[Activation]:
        name = name.lower()
        if name not in cls._registry:
            raise ValueError(f"Activation '{name}' not found in registry")
        return cls._registry[name]
