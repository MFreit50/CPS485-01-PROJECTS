from typing import List

import pytest

from src.producers.nn.losses.base import Loss
from src.producers.nn.losses.registry import LossRegistry


def test_known_losses():
    # known losses should be loaded into the registry at import
    # this test checks that they really are there and can be retrieved
    loss_registry = LossRegistry()
    for name in ["mse", "bce"]:
        loss_cls = loss_registry.get(name)
        assert loss_cls is not None


def test_unknown_loss():
    loss_registry = LossRegistry()
    with pytest.raises(ValueError):
        loss_registry.get("unknown_loss")


def test_case_insensitivity():
    loss_registry = LossRegistry()
    for name in ["mse", "bce"]:
        loss_lower = loss_registry.get(name.lower())
        loss_upper = loss_registry.get(name.upper())
        assert loss_lower == loss_upper


def test_register_new_loss():
    class DummyLoss(Loss):
        def compute(self, predicted: List[float], expected: List[float]) -> float:
            return 1.0

        def derivative(
            self, predicted: List[float], expected: List[float]
        ) -> List[float]:
            return [1.0] * len(predicted)

    LossRegistry.register("dummy", DummyLoss)
    retrieved_cls = LossRegistry.get("dummy")
    assert retrieved_cls == DummyLoss
