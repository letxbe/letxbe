import secrets

from letxbe.type.page import BBox, ImageFormat, ImageProperties, Word


def test_image_properties():
    # Given
    width = secrets.randbelow(100)
    height = secrets.randbelow(100)
    fmt = ImageFormat.TIFF

    # When
    img_properties = ImageProperties(size=(width, height), format=fmt)

    # Then
    assert isinstance(img_properties, ImageProperties)
    assert img_properties.rotation == 0


def test_word__by_alias_or_not():
    # Given
    confidence = secrets.randbelow(100)
    bbox = BBox(x0=0, x1=1, y0=1, y1=1)
    caption = "way"

    word_alias_dict = {
        "confidence": confidence,
        "bbox": bbox.dict(),
        "word-caption": caption,
    }

    word_no_alias_dict = {
        "confidence": confidence,
        "bbox": bbox.dict(),
        "word_caption": caption,
    }

    # When
    word_alias = Word(**word_alias_dict)
    word_no_alias = Word(**word_no_alias_dict)

    # Then
    assert word_alias == word_no_alias
