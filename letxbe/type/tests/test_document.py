import pytest
from pydantic import ValidationError

from letxbe.type.document import Form


@pytest.mark.parametrize(
    "dict_obj, raises_validation_error",
    [
        ({"a": 0}, False),
        ({"result": {"a": [[0]]}}, True),
        ({"result": {"a": [{"b": 0}]}}, True),
        ({"result": {"a": {"b": ["c", "d"]}}}, False),
    ],
)
def test_form_validation_error(dict_obj, raises_validation_error):
    if raises_validation_error:
        with pytest.raises(ValidationError):
            Form.parse_obj(dict_obj)
    else:
        Form.parse_obj(dict_obj)


def test_form(form_dict):
    assert form_dict == Form(**form_dict).dict()
