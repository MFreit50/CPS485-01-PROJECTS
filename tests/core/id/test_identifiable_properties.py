from typing import Hashable

from src.core.id.identifiable import Identifiable


def test_raw_id_is_hashable():
    instance = Identifiable()
    assert isinstance(instance.raw_id, Hashable)


def test_id_is_string():
    instance = Identifiable()
    assert isinstance(instance.id, str)
