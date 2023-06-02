from letxbe.type.target import Target


def test_target(target_dict):
    assert target_dict == Target(**target_dict).dict()
