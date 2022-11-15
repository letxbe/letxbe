import pytest
from pydantic import ValidationError, parse_obj_as

from letxbe.type.base import DatedMixin, ValueType, assert_type_and_value_equality


@pytest.mark.parametrize("value", [True, False])
def test_ValueType__parse_is_bool(value):
    assert type(parse_obj_as(ValueType, value)).__name__ == "bool"


@pytest.mark.parametrize("value", [1, 0])
def test_ValueType__parse_is_int(value):
    assert type(parse_obj_as(ValueType, value)).__name__ == "int"


@pytest.mark.parametrize("value", [0.0, 1.2])
def test_ValueType__parse_is_float(value):
    assert type(parse_obj_as(ValueType, value)).__name__ == "float"


@pytest.mark.parametrize("value", ["", "dkqshf"])
def test_ValueType__parse_is_str(value):
    assert type(parse_obj_as(ValueType, value)).__name__ == "str"


def test_ValueType__None_not_accepted():
    with pytest.raises(ValidationError):
        parse_obj_as(ValueType, None)


@pytest.mark.parametrize(
    "label_1,label_2",
    [
        ("test", "test"),
        (0, 0),
        (False, False),
        (1, 1),
        (True, True),
    ],
)
def test_assert_type_and_value_equality(label_1, label_2):
    assert_type_and_value_equality(label_1, label_2)


@pytest.mark.parametrize(
    "label_1,label_2",
    [
        ("test", 1),
        (0, False),
        (False, ""),
        (True, 1),
        (True, "un texte"),
    ],
)
def test_assert_type_and_value_equality__raise(label_1, label_2):
    with pytest.raises(AssertionError):
        assert_type_and_value_equality(label_1, label_2)


def test_read_created_at_and_updated_at():
    # When
    dated_1 = DatedMixin(created_at=1)

    assert dated_1.created_at == 1
    assert dated_1.updated_at != dated_1.created_at
