import pytest

from src.producers.nn.activations.base import Activation
from src.producers.nn.activations.registry import ActivationRegistry


def test_known_activations():
    # known activations should be loaded into the registry at import
    # this test checks that they really are there and can be retrieved
    activation_registry = ActivationRegistry()
    for name in ["sigmoid", "tanh", "relu"]:
        activation_cls = activation_registry.get(name)
        assert activation_cls is not None


def test_unknown_activation():
    activation_registry = ActivationRegistry()
    with pytest.raises(ValueError):
        activation_registry.get("unknown_activation")


def test_case_insensitivity():
    activation_registry = ActivationRegistry()
    for name in ["sigmoid", "tanh", "relu"]:
        activation_lower = activation_registry.get(name.lower())
        activation_upper = activation_registry.get(name.upper())
        assert activation_lower == activation_upper


def test_register_new_activation():
    class DummyActivation(Activation):
        def compute(self, z: float) -> float:
            return z

        def derivative(self, a: float) -> float:
            return 1.0

    ActivationRegistry.register("dummy", DummyActivation)
    retrieved_cls = ActivationRegistry.get("dummy")
    assert retrieved_cls == DummyActivation
