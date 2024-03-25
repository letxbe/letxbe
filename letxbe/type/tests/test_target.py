from letxbe.type.enum import ActionCode, DocumentStatus
from letxbe.type.target import Target


def test_target(target_dict):
    assert target_dict == Target(**target_dict).dict()


def test_target__has_no_enum_values():
    # Given
    target_dict = {
        "created_at": 123456789,
        "slug": "dkjsvkdfvdef",
        "extension": "pdf",
        "name": "some name",
        "urn": "wxcvbnvmlkj",
        "role": None,
        "status_code": DocumentStatus.PROCESSING,
        "action_code": ActionCode.PROJECTION,
    }
    assert Target(**target_dict).dict() == {
        "artefact": {},
        "status_code": "103",
        "action_code": "projection",
        "exception": None,
        "parent": None,
        "role": None,
        "prediction": {
            "model_version": None,
            "score": None,
            "comment": "",
            "result": {},
        },
        "feedback": None,
        "current": {"result": {}},
        "client_env": "test",
        "form": {"result": {}},
        "extension": "pdf",
        "slug": "dkjsvkdfvdef",
        "created_at": 123456789,
        "name": "some name",
        "urn": "wxcvbnvmlkj",
    }
