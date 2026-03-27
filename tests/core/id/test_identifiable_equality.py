from src.core.id.identifiable import Identifiable
from tests.core.id.mock_id_generator import make_mock_generator


class AnotherIdentifiable(Identifiable):
    """
    Test Class used for cmoparing equality
    """

    pass


def test_same_instance_is_equal_to_itself():
    instance = Identifiable()
    assert instance == instance


def test_two_instances_with_different_ids_are_not_equal():
    a = Identifiable()
    b = Identifiable()
    assert a != b


def test_two_instances_with_same_id_are_equal():
    generator = make_mock_generator("same-id")
    a = Identifiable(id_generator=generator)
    generator.generate_id.return_value = "same-id"
    b = Identifiable(id_generator=generator)
    assert a == b


def test_different_types_with_same_id_are_not_equal():
    generator = make_mock_generator("same-id")
    a = Identifiable(id_generator=generator)
    generator.generate_id.return_value = "same-id"
    b = AnotherIdentifiable(id_generator=generator)
    assert a != b


def test_equality_with_non_identifiable_returns_not_implemented():
    instance = Identifiable()
    result = instance.__eq__("not an identifiable")
    assert result is NotImplemented
