import pytest
from pydantic import ValidationError

from letxbe.type.label import (
    BBoxInPageClue,
    Current,
    CurrentResultType,
    Feedback,
    FeedbackResultType,
    Label,
    LabelFeedback,
    LabelPrediction,
    Prediction,
    PredictionResultType,
    WordClue,
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
        LABEL_BASE = {"score": None, "model_version": None}
    elif result_type == FeedbackResultType:
        LABEL_BASE = {"source": None, "vote": "Valid"}
    else:
        LABEL_BASE = {}

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
        LABEL_BASE = {"score": None, "model_version": None}
    elif result_type == FeedbackResultType:
        LABEL_BASE = {"source": None, "vote": "Valid"}
    else:
        LABEL_BASE = {}

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


def test_bbox_in_page_clue(bbox_in_page_clue_dict):
    assert bbox_in_page_clue_dict == BBoxInPageClue(**bbox_in_page_clue_dict).dict()


def test_word_clue(word_clue_dict):
    assert word_clue_dict == WordClue(**word_clue_dict).dict()


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
