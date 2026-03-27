from src.core.id.identifiable import Identifiable
from tests.core.id.mock_id_generator import make_mock_generator


def test_instance_is_hashable():
    instance = Identifiable()
    assert isinstance(hash(instance), int)


def test_same_id_produces_same_hash():
    generator = make_mock_generator("same-id")
    a = Identifiable(id_generator=generator)
    generator.generate_id.return_value = "same-id"
    b = Identifiable(id_generator=generator)
    assert hash(a) == hash(b)


def test_different_ids_produce_different_hashes():
    a = Identifiable()
    b = Identifiable()
    assert hash(a) != hash(b)


def test_instance_usable_as_dict_key():
    instance = Identifiable()
    d = {instance: "value"}
    assert d[instance] == "value"


def test_instance_usable_in_set():
    a = Identifiable()
    b = Identifiable()
    s = {a, b}
    assert len(s) == 2
