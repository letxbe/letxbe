import math
from typing import Dict, List, Tuple, Union

from letxbe.provider.type import Prediction
from letxbe.utils import pydantic_model_to_json

from .type import SaverArgType

MAX_SAVER_LIST_LEN = 10


# TODO refacto and add unit tests
def split_data_into_batches(data: Tuple[SaverArgType]) -> List[Union[list, dict, None]]:
    """
    Slit data into a list of tuples with maximum `MAX_SAVER_LIST_LEN` elements.

    Args:
        data (Tuple[SaverArgType]): a tuple of `SaverArgType` objects

    Returns:
        a list of tuples of `SaverArgType` objects
    """

    first_shift = 0
    shift_map: Dict[int, Dict[int, Union[list, dict]]] = {first_shift: {}}

    for vec_idx, element in enumerate(data):

        if isinstance(element, Prediction):
            shift_map[first_shift][vec_idx] = pydantic_model_to_json(element)
            continue

        if isinstance(element, list):
            shifts = math.ceil(len(element) / MAX_SAVER_LIST_LEN)
            if shifts == 0:
                shift_map[first_shift][vec_idx] = []
                continue

            for shift in range(shifts):
                if shift not in shift_map:
                    shift_map[shift] = {}
                shift_map[shift][vec_idx] = [
                    pydantic_model_to_json(nested)
                    for nested in element[
                        shift * MAX_SAVER_LIST_LEN : (shift + 1) * MAX_SAVER_LIST_LEN
                    ]
                ]
            continue

        raise ValueError("Element must be an instance of `SaverArgType`.")

    vec_size = len(shift_map[first_shift])
    vec_idxs = range(vec_size)

    vecs = []
    for shift, vector_with_hole in shift_map.items():
        if vec_size == 1:
            vecs += [vector_with_hole.get(0, None)]
            continue
        vecs += [[vector_with_hole.get(idx, None) for idx in vec_idxs]]
    return vecs
