import pytest


@pytest.fixture
def form_dict():
    return {
        "result": {
            "address": {
                "principal": True,
                "street": "41 rue Beauregard",
                "zip code": 75002,
            },
            "artefacts": ["customers", "orders"],
            "version": 1.2,
        }
    }


@pytest.fixture
def bbox_in_page_clue_dict():
    return {
        "value": "exemplaire",
        "role": None,
        "page_idx": 0,
        "bbox": {
            "x0": 0.7011789679527283,
            "x1": 0.7779027447104454,
            "y0": 0.5617986917495728,
            "y1": 0.573211207985878,
        },
    }


@pytest.fixture
def word_clue_dict():
    return {
        "value": "exemplaire",
        "role": None,
        "page_idx": 0,
        "line_idx": 1,
        "word_idx": 2,
        "bbox": {
            "x0": 0.7011789679527283,
            "x1": 0.7779027447104454,
            "y0": 0.5617986917495728,
            "y1": 0.573211207985878,
        },
    }


@pytest.fixture
def prenom_label_prediction_dict(word_clue_dict):
    return {
        "lid": "d66f48a0-980c-43ae-a60d-686a48628191",
        "value": "Exemplaire",
        "clues": [word_clue_dict],
        "score": 100.0,
        "model_version": None,
        "children": None,
    }


@pytest.fixture
def date_label_prediction_dict(bbox_in_page_clue_dict):
    return {
        "lid": "3aeb2502-8bc4-473d-a143-4874f9919c4c",
        "value": 1651363200000,
        "clues": [bbox_in_page_clue_dict],
        "score": None,
        "model_version": None,
        "children": None,
    }


@pytest.fixture
def prediction_result_dict(prenom_label_prediction_dict, date_label_prediction_dict):
    return {
        "prenom": prenom_label_prediction_dict,
        "date": date_label_prediction_dict,
        "clients": [
            {
                "client_1": {
                    "lid": "aead458b-07b8-4ded-a53f-b04a55a679e3",
                    "value": "QWE123",
                    "clues": [],
                    "children": None,
                    "score": 98.1,
                    "model_version": None,
                },
                "client_2": {
                    "lid": "2fe3133e-2745-4b66-82db-c0dd612e5f69",
                    "value": "QWE125",
                    "clues": [],
                    "children": None,
                    "score": 98.2,
                    "model_version": None,
                },
            },
        ],
        "externe": {
            "fournisseurs": {
                "fournisseur_1": {
                    "lid": "aead458b-07b8-4ded-a53f-b04a55a679e0",
                    "value": "F4567",
                    "clues": [],
                    "children": None,
                    "score": 98.3,
                    "model_version": None,
                },
            },
        },
    }


@pytest.fixture
def prediction_dict(prediction_result_dict):
    return {
        "model_version": "v0.0",
        "score": None,
        "comment": "",
        "result": prediction_result_dict,
    }


@pytest.fixture
def prenom_label_feedback_dict():
    return {
        "lid": "3aeb2502-8bc4-473d-a143-4874f9918880",
        "value": "Exemplaire",
        "clues": [],
        "children": None,
        "source": None,
        "vote": "Valid",
    }


@pytest.fixture
def date_label_feedback_dict():
    return {
        "lid": "3aeb2502-8bc4-473d-a143-4874f9918888",
        "value": 1651363299999,
        "clues": [],
        "children": None,
        "source": None,
        "vote": "Invalid",
    }


@pytest.fixture
def feedback_result_dict(prenom_label_feedback_dict, date_label_feedback_dict):
    return {
        "prenom": prenom_label_feedback_dict,
        "date": date_label_feedback_dict,
        "clients": [
            {
                "lid": "3aeb2502-8bc4-473d-a143-4874f9917780",
                "value": "QWE000",
                "clues": [],
                "children": None,
                "source": None,
                "vote": "Invalid",
            }
        ],
        "externe": {
            "fournisseurs": {
                "fournisseur_1": {
                    "lid": "3aeb2502-8bc4-473d-a143-4874f9917780",
                    "value": "F4567",
                    "clues": [],
                    "children": None,
                    "source": None,
                    "vote": "Valid",
                }
            }
        },
    }


@pytest.fixture
def feedback_dict(feedback_result_dict):
    return {
        "comment": "",
        "result": feedback_result_dict,
    }


@pytest.fixture
def prenom_label_dict():
    return {
        "lid": "d66f48a0-980c-43ae-a60d-000a48628191",
        "value": "Exemplaire",
        "clues": [],
        "children": None,
    }


@pytest.fixture
def date_label_dict():
    return {
        "lid": "d66f48a0-980c-43ae-a60d-000a48628191",
        "value": "1651363299999",
        "clues": [],
        "children": None,
    }


@pytest.fixture
def current_result_dict(prenom_label_dict, date_label_dict):
    return {
        "prenom": prenom_label_dict,
        "date": date_label_dict,
        "clients": [
            {
                "client_1": {
                    "lid": "3aeb2502-8bc4-473d-a143-4567f9917780",
                    "value": "QWE000",
                    "clues": [],
                    "children": None,
                },
                "client_2": {
                    "lid": "2fe3133e-2745-4b66-82db-gggg612e5f69",
                    "value": "QWE125",
                    "clues": [],
                    "children": None,
                },
            }
        ],
        "fournisseurs": {
            "fournisseur_1": {
                "lid": "3aeb2502-8bc4-473d-a143-4874f9917780",
                "value": "F4567",
                "clues": [],
                "children": None,
            }
        },
    }


@pytest.fixture
def current_dict(current_result_dict):
    return {
        "result": current_result_dict,
    }


@pytest.fixture
def target_dict(form_dict, prediction_dict, feedback_dict, current_dict):
    return {
        "created_at": 123456789,
        "slug": "dkjsvkdfvdef",
        "client_env": "test",
        "form": form_dict,
        "extension": "pdf",
        "name": "azerty.pdf",
        "urn": "WXCVBNVMLKJ",
        "role": None,
        "prediction": prediction_dict,
        "feedback": feedback_dict,
        "current": current_dict,
        "parent": None,
        "status_code": "103",
        "action_code": "prediction",
        "exception": None,
        "artefact": {},
    }
