from typing import Dict, Type

from src.producers.nn.losses.base import Loss


class LossRegistry:
    _registry: Dict[str, Type[Loss]] = {}

    @classmethod
    def register(cls, name: str, loss_cls: Type[Loss]) -> None:
        cls._registry[name.lower()] = loss_cls

    @classmethod
    def get(cls, name: str) -> Type[Loss]:
        name = name.lower()
        if name not in cls._registry:
            raise ValueError(f"Loss '{name}' not found in registry")
        return cls._registry[name]
