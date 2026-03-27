import pytest

from src.core.id.identifiable import Identifiable
from tests.core.id.mock_id_generator import make_mock_generator


def test_raises_if_called_after_init():
    instance = Identifiable()
    with pytest.raises(RuntimeError, match="called more than once"):
        instance._initialize_id()


def test_raises_if_called_twice_directly():
    """Simulates frozen dataclass path being called twice."""
    instance = object.__new__(Identifiable)
    instance._initialize_id()
    with pytest.raises(RuntimeError, match="called more than once"):
        instance._initialize_id()


def test_initializes_correctly_without_init():
    instance = object.__new__(Identifiable)
    generator = make_mock_generator("frozen-id")
    instance._initialize_id(generator)
    assert instance.raw_id == "frozen-id"
    assert instance.id == "frozen-id"


def test_uses_default_generator_when_none_passed():
    instance = object.__new__(Identifiable)
    instance._initialize_id()
    assert instance.raw_id is not None
    assert isinstance(instance.id, str)
