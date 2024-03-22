from letxbe.utils import generate_short_unique_id


def test_generate_short_unique_id():
    # When
    short_id = generate_short_unique_id()

    # Then
    assert isinstance(short_id, str)
    assert len(short_id) == 12
