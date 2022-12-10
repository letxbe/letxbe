from letxbe.type.document import Form


def test_form():
    expected = {"result": {"a": {"b": ["c", "d"]}}}
    parsed = Form.parse_obj(expected).dict()

    assert expected == parsed
