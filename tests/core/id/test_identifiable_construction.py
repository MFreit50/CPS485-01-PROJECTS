from src.core.id.identifiable import Identifiable
from tests.core.id.mock_id_generator import make_mock_generator


def test_default_generator_assigns_raw_id():
    instance = Identifiable()
    assert instance.raw_id is not None


def test_default_generator_assigns_id_string():
    instance = Identifiable()
    assert isinstance(instance.id, str)
    assert len(instance.id) > 0


def test_id_string_is_str_of_raw_id():
    instance = Identifiable()
    assert instance.id == str(instance.raw_id)


def test_custom_generator_is_used():
    generator = make_mock_generator("custom-id")
    instance = Identifiable(id_generator=generator)
    assert instance.raw_id == "custom-id"
    assert instance.id == "custom-id"


def test_custom_generator_called_exactly_once():
    generator = make_mock_generator("x")
    Identifiable(id_generator=generator)
    generator.generate_id.assert_called_once()


def test_two_instances_have_different_ids():
    a = Identifiable()
    b = Identifiable()
    assert a.id != b.id
    assert a.raw_id != b.raw_id
