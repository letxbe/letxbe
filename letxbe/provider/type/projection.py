from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, root_validator

from letxbe.type.base import ValueType


class __ProjectionBase(BaseModel):
    """
    Define base for all elements in Projection.result.

    Related to :

    Projection: Uses `Projection.calculate_projection_entry` to set projection_entry.

    Prediction: Use `projection_entry` to associate a ProjectionMap to a prediction using a ProjectionClue.
    Use `extract_remaining_projection_structure_from_entry_point` in flow.service.projection to find ProjectionMap based on projection_entry stored in a clue.

    projection_entry: identifier for a ProjectionMap inside a Projection structure.
        this identifier is not stored in database but calculated when instanciating Projection.
    """

    projection_entry: str = ""


class ProjectionField(__ProjectionBase):
    """
    Args:
        value (ValueType): the value of a field
    """

    value: Optional[ValueType]

    @root_validator
    def calculate_projection_entry(cls: Any, values: Dict) -> Dict:
        """
        Calculate `projection_entry`.
        """
        values["projection_entry"] = ""

        return values


class ProjectionMap(__ProjectionBase):
    """
    Represent a recursive data structure stored in document.projection that can be pointed to in a Clue.

    Uses `ProjectionMap.update_forward_refs()` (below) to make it recursive.

    result: (Dict): a mapping that associates field_key to Field or a list of Field
    """

    result: Dict[str, "ProjectionMapValueType"]


ProjectionMapValueType = Union[
    List[ProjectionMap], List[ProjectionField], ProjectionMap, ProjectionField
]

ProjectionMap.update_forward_refs()


class ProjectionRoot(ProjectionMap):
    """
    Defines the content of Target or Artefact that corresponds to a line in a table or flat JSON form.
    Fields may be a list of values with the same type.

    Be carefull that xid must abide : https://www.arangodb.com/docs/stable/data-modeling-naming-conventions-document-keys.html

    slug (str): a unique identifier that can be used inside a request pathname
    xid (str): a unique identifier that can be provided by clients
    result: (Dict): a mapping that associates field_key to Field or a list of Field

    # TODO : ensure xid abides following link with a test : https://www.arangodb.com/docs/stable/data-modeling-naming-conventions-document-keys.html
    """

    xid: str

    @root_validator
    def calculate_projection_entry(cls: Any, values: Dict) -> Dict:
        """
        Calculate `projection_entry` recursively for ProjectionMaps in object.result.
        """

        def _recurse(
            projection_map_result: Dict[str, ProjectionMapValueType],
            projection_location: Optional[str],
        ) -> None:

            for key, projection in projection_map_result.items():
                if isinstance(projection, list):
                    for index, element in enumerate(projection):
                        if projection_location is None:
                            location = f"{key}[{index}]"
                        else:
                            location = f"{projection_location}.{key}[{index}]"
                        element.projection_entry = location
                        if isinstance(element, ProjectionMap):
                            _recurse(element.result, location)
                else:
                    if projection_location is None:
                        location = f"{key}"
                    else:
                        location = f"{projection_location}.{key}"
                    projection.projection_entry = location
                    if isinstance(projection, ProjectionMap):
                        _recurse(projection.result, location)

        _recurse(values.get("result", {}), None)

        return values
