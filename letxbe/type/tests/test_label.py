from letxbe.type.label import PredictionResultType
from letxbe.utils import pydantic_model_to_json


def test_prediction_result_type_recursive():
    # Given
    result = {
        "tables": [
            {
                "edge": {
                    "lid": "e1e103a1-102c-43ee-9bde-06036f4b36ef",
                    "value": "ciao",
                    "clues": [],
                    "score": None,
                    "model_version": None,
                    "children": None,
                },
                "shape": [
                    {
                        "lid": "bc2ed26c-0bbc-4da8-b58c-7dbe3e5ca65d",
                        "value": 123,
                        "clues": [],
                        "score": None,
                        "model_version": None,
                        "children": None,
                    },
                    {
                        "lid": "bc2ed26c-0bbc-4da8-b58c-06036f4b36ef",
                        "value": 23,
                        "clues": [],
                        "score": None,
                        "model_version": None,
                        "children": None,
                    },
                ],
            }
        ]
    }

    # When
    prtype = PredictionResultType(__root__=result)

    # Then
    assert pydantic_model_to_json(prtype) == result
