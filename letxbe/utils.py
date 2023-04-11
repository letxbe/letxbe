import io
import json
import re
from typing import List, Sequence, Tuple, Union, cast
from zipfile import ZipFile, is_zipfile

import requests
from PIL.Image import Image
from pydantic import BaseModel


def pil_image_to_bytes(image: Image) -> bytes:
    # https://stackoverflow.com/a/33117447
    imgByteIO = io.BytesIO()
    image.save(imgByteIO, format=image.format)

    return cast(bytes, imgByteIO.getvalue())


def extract_filename_from_response_header(res: requests.Response) -> str:
    d = res.headers["content-disposition"]
    filename = re.findall("filename=(.+)", d)[0]

    if isinstance(filename, str):
        return filename

    raise ValueError("Cannot find filename.")


def pydantic_model_to_json(model: BaseModel) -> dict:
    """
    Convert any model to a json that can be used as a query parameter for arangodb.

    It is however preferable to create requests that do not take json as a query
    parameter but go explicitly inside the structure.

    When using .dict(), some types including enums seem to not be exported as strings.

    Args:
        model (BaseModel): Pydantic model to convert.

    Returns:
        Dictionary representation of a model.
    """
    return cast(dict, json.loads(model.json()))


def pydantic_model_to_bytes(model: Union[BaseModel, Sequence[BaseModel]]) -> bytes:
    """
    Convert any pydantic model (or list of models) to bytes.

    Usage examples:
        - the Page list to be uploaded to the bucket via boto_sdk

    Args:
        model (Union[BaseModel, List[BaseModel]): Pydantic model to convert or list
            of models.

    Returns:
        bytes representation of the model
    """
    if isinstance(model, list):
        serializable_file: Union[list, dict] = [mod.dict() for mod in model]
    elif isinstance(model, BaseModel):
        serializable_file = model.dict()
    else:
        raise TypeError("Input must be a pydantic model or a list of pydantic models")

    return json.dumps(serializable_file).encode("utf-8")


def bytes_to_zipfile(
    zipped_bytes: bytes,
) -> ZipFile:
    """
    Convert bytes to a ZipFile, when compatible.
    """

    zip_stream = io.BytesIO(zipped_bytes)

    if not is_zipfile(zip_stream):
        raise ValueError("Bytes in file do not correspond to a zipped file.")

    return ZipFile(zip_stream)


def zipfile_to_byte_files(
    zipped: ZipFile,
) -> List[Tuple[str, bytes]]:
    """
    Convert ZipFile to a list of tuples with filename and bytes.
    """

    filenames = zipped.namelist()

    res = []
    for name in filenames:
        res += [(name, zipped.open(name).read())]

    return res


def zip_files(
    tuples_with_filename_and_bytes: List[Tuple[str, bytes]],
) -> bytes:

    zip_stream = io.BytesIO()

    with ZipFile(zip_stream, "w") as zip_archive:
        for imported in tuples_with_filename_and_bytes:
            zip_archive.writestr(*imported)

    return zip_stream.getvalue()
