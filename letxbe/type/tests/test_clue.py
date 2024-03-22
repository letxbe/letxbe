import secrets

import pytest

from letxbe.type.clue import BBoxInPageClue, ShapeClue, WordClue


def test_bbox_in_page_clue(bbox_in_page_clue_dict):
    assert bbox_in_page_clue_dict == BBoxInPageClue(**bbox_in_page_clue_dict).dict()


def test_word_clue(word_clue_dict):
    assert word_clue_dict == WordClue(**word_clue_dict).dict()


def test_shape_clue__raise_value_error(bbox__with_zeros):
    # Given
    odd_number_of_points = 2 * secrets.randbelow(10) + 3
    too_small_to_be_a_polygon = [123, 123]
    # Then
    with pytest.raises(ValueError):
        ShapeClue(
            page_idx=0,
            value="",
            bbox=bbox__with_zeros,
            polygon=too_small_to_be_a_polygon,
        )

    with pytest.raises(ValueError):
        ShapeClue(
            page_idx=0,
            value="",
            bbox=bbox__with_zeros,
            polygon=[secrets.randbelow(100) for _ in range(1, odd_number_of_points)],
        )


def test_shape_clue__empty_polygon(bbox__with_zeros):
    # When
    shape_clue = ShapeClue(page_idx=0, value="", bbox=bbox__with_zeros)

    # Then
    assert shape_clue.polygon == []
    assert shape_clue.bbox == bbox__with_zeros
