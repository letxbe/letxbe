import pytest
from pydantic import ValidationError

from letxbe.type.label import (
    Current,
    CurrentResultType,
    Feedback,
    FeedbackResultType,
    Label,
    LabelFeedback,
    LabelPrediction,
    LabelType,
    Prediction,
    PredictionResultType,
)
from letxbe.utils import pydantic_model_to_json


@pytest.mark.parametrize(
    "result_type",
    [
        PredictionResultType,
        CurrentResultType,
        FeedbackResultType,
    ],
)
def test_result_type_recursive(result_type):
    if result_type == PredictionResultType:
        LABEL_BASE = {"score": None, "model_version": None, "label_type": "prediction"}
    elif result_type == FeedbackResultType:
        LABEL_BASE = {"source": None, "vote": "Valid", "label_type": "feedback"}
    else:
        LABEL_BASE = {"label_type": None}

    # Given
    result = {
        "tables": [
            {
                "nested_tables": [
                    {
                        "edge": {
                            **LABEL_BASE,
                            "lid": "e1e103a1-102c-43ee-9bde-06036f4b36ef",
                            "value": "ciao",
                            "clues": [],
                            "children": None,
                        },
                        "shape": [
                            {
                                **LABEL_BASE,
                                "lid": "bc2ed26c-0bbc-4da8-b58c-7dbe3e5ca65d",
                                "value": 123,
                                "clues": [],
                                "children": None,
                            },
                            {
                                **LABEL_BASE,
                                "lid": "bc2ed26c-0bbc-4da8-b58c-06036f4b36ef",
                                "value": 23,
                                "clues": [],
                                "children": None,
                            },
                        ],
                    },
                    {
                        "edge": {
                            **LABEL_BASE,
                            "lid": "e1e103a1-10qsdf2c-sqf-9bde-asdfqf",
                            "value": "ciao2",
                            "clues": [],
                            "children": None,
                        },
                        "shape": [
                            {
                                **LABEL_BASE,
                                "lid": "qsdfxq-qsdf-qsdf-qsdf-7dbe3e5ca65d",
                                "value": 123,
                                "clues": [],
                                "children": None,
                            },
                            {
                                **LABEL_BASE,
                                "lid": "qsdfqfdsf-0bbc-zfzf-wxf-dsqfqdfs",
                                "value": 23,
                                "clues": [],
                                "children": None,
                            },
                        ],
                    },
                ]
            }
        ]
    }

    # When
    prtype = result_type(__root__=result)

    # Then
    assert pydantic_model_to_json(prtype) == result


@pytest.mark.parametrize(
    "result_type",
    [
        PredictionResultType,
        CurrentResultType,
        FeedbackResultType,
    ],
)
def test_prediction_result_type__table(result_type):
    if result_type == PredictionResultType:
        LABEL_BASE = {"score": None, "model_version": None, "label_type": "prediction"}
    elif result_type == FeedbackResultType:
        LABEL_BASE = {"source": None, "vote": "Valid", "label_type": "feedback"}
    else:
        LABEL_BASE = {"label_type": None}

    # Given
    result = {
        "tables": [
            [
                {
                    **LABEL_BASE,
                    "lid": "e1e103a1-102c-43ee-9bde-06036f4b36ef",
                    "value": "ciao",
                    "clues": [],
                    "children": None,
                }
            ]
        ]
    }

    # When
    prtype = result_type(__root__=result)

    # Then
    assert pydantic_model_to_json(prtype) == result

    # Given
    result = {
        "tables": [
            [
                [
                    {
                        **LABEL_BASE,
                        "lid": "e1e103a1-102c-43ee-9bde-06036f4b36ef",
                        "value": "ciao",
                        "clues": [],
                        "children": None,
                    }
                ]
            ]
        ]
    }

    # When
    prtype = result_type(__root__=result)

    # Then
    assert pydantic_model_to_json(prtype) == result

    # Given
    result = {
        "tables": [
            [
                [
                    [
                        {
                            **LABEL_BASE,
                            "lid": "e1e103a1-102c-43ee-9bde-06036f4b36ef",
                            "value": "ciao",
                            "clues": [],
                            "children": None,
                        }
                    ]
                ]
            ]
        ]
    }

    # When
    with pytest.raises(ValidationError):
        _ = result_type(__root__=result)


def test_label_prediction(prenom_label_prediction_dict, date_label_prediction_dict):
    assert (
        prenom_label_prediction_dict
        == LabelPrediction(**prenom_label_prediction_dict).dict()
    )
    assert (
        date_label_prediction_dict
        == LabelPrediction(**date_label_prediction_dict).dict()
    )


def test_prediction(prediction_dict):
    assert prediction_dict == Prediction(**prediction_dict).dict()


def test_label_feedback(prenom_label_feedback_dict, date_label_feedback_dict):
    assert (
        prenom_label_feedback_dict == LabelFeedback(**prenom_label_feedback_dict).dict()
    )
    assert date_label_feedback_dict == LabelFeedback(**date_label_feedback_dict).dict()


def test_feedback(feedback_dict):
    assert feedback_dict == Feedback(**feedback_dict).dict()


def test_label(prenom_label_dict, date_label_dict):
    assert prenom_label_dict == Label(**prenom_label_dict).dict()
    assert date_label_dict == Label(**date_label_dict).dict()


def test_current(current_dict):
    assert current_dict == Current(**current_dict).dict()


def test_prediction__has_no_enum_values():
    # Given
    lp_dict = {
        "label_type": LabelType.PREDICTION,
        "lid": "wum41149ux68",
        "score": 0.85,
    }
    label_prediction = LabelPrediction(**lp_dict)
    prediction = Prediction(**{"result": {"some_label": label_prediction}})

    # Then
    print(label_prediction.dict())
    print(prediction.dict())
    assert label_prediction.dict() == {
        "label_type": "prediction",
        "lid": "wum41149ux68",
        "value": None,
        "clues": [],
        "children": None,
        "score": 0.85,
        "model_version": None,
    }
    assert prediction.dict() == {
        "model_version": None,
        "score": None,
        "comment": "",
        "result": {
            "some_label": {
                "label_type": "prediction",
                "lid": "wum41149ux68",
                "value": None,
                "clues": [],
                "children": None,
                "score": 0.85,
                "model_version": None,
            }
        },
    }
