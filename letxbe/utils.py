import io
import json
import re
from typing import List, Tuple, cast
from zipfile import ZipFile, is_zipfile

import requests
from pydantic import BaseModel


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
