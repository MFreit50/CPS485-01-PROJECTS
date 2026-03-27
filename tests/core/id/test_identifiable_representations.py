from src.core.id.identifiable import Identifiable


def test_repr_contains_class_name():
    instance = Identifiable()
    assert "Identifiable" in repr(instance)


def test_repr_contains_full_id():
    instance = Identifiable()
    assert instance.id in repr(instance)


def test_str_contains_class_name():
    instance = Identifiable()
    assert "Identifiable" in str(instance)


def test_str_contains_truncated_id():
    instance = Identifiable()
    assert instance.id[:8] in str(instance)


def test_str_contains_ellipsis():
    instance = Identifiable()
    assert "..." in str(instance)
