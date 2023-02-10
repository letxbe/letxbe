import math
from typing import Dict, List, Tuple, Union

import requests

from letxbe.exception import AutomationError
from letxbe.provider.type import Page, Prediction, Projection
from letxbe.session import LXBSession
from letxbe.utils import bytes_to_zipfile, pydantic_model_to_json, zipfile_to_byte_files

from .type import DownloadResource, LogStatus, SaverArgType, ServiceUrl, Task

MAX_SAVER_LIST_LEN = 10


def split_to_vecs(data: Tuple[SaverArgType]) -> list:
    """
    Slit a tuple of `SaverArgType` objects into a list of tuples with fewer elements each
      in order to save it components in batches.
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


class Provider(LXBSession):
    """
    Connect to LetXbe and share requests.
    """

    def __init__(self, session: LXBSession, provider_urn: str):
        self.__session = session
        self.__urn = provider_urn

    @property
    def session(self) -> LXBSession:
        return self.__session

    @property
    def urn(self) -> str:
        return self.__urn

    def take_charge(
        self,
    ) -> Task:
        """
        Take charge for the next task to be executed by the service provider.

        Returns:
            A Task object.
        """

        response = requests.post(
            url=self.session.server + ServiceUrl.TASKS.format(provider=self.urn),
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        return Task.parse_obj(response.json())

    def _save(
        self,
        task_slug: str,
        data: Union[list, dict],
    ) -> None:
        """
        Save outcome from a task.

        Multiple saves can be made before finishing.

        Returns:
            Text of the HTTP response.
        """

        response = requests.post(
            url=self.session.server
            + ServiceUrl.SAVE.format(provider=self.urn, task=task_slug),
            json=data,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        if "success" in response.json():
            return

        raise AutomationError(f"Error in response: {response}")

    def _finish(
        self, task_slug: str, status_code: LogStatus, text: str, exception: str
    ) -> None:
        """
        End a task to be executed by service.

        Args:
            task_slug (str) : a task slug.
            status_code (LogStatus) : status of the process outcome.
            text (str) : a detailed log to store eventual warnings or errors.
            exception (str) : a short exception to show on the front-end.

        Returns:
            Text of the HTTP response.
        """

        data = {
            "status_code": status_code.value,
            "text": text,
            "exception": exception,
        }

        response = requests.post(
            url=self.session.server
            + ServiceUrl.FINISH.format(provider=self.urn, task=task_slug),
            headers=self.session.authorization_header,
            data=data,
        )

        self.session._verify_status_code(response)

        if "success" in response.json():
            return

        raise AutomationError(f"Error in response: {response}")

    def save_and_finish(
        self,
        task_slug: str,
        data: Tuple[SaverArgType],
        status_code: LogStatus = LogStatus.SUCCESS,
        text: str = "",
        exception: str = "",
    ) -> None:

        vectors = split_to_vecs(data)

        for vector in vectors:
            self._save(task_slug, vector)

        self._finish(
            task_slug=task_slug, status_code=status_code, text=text, exception=exception
        )

    def download_document_file(
        self,
        task_slug: str,
        role: Optional[str] = None
    ) -> List[Tuple[str, bytes]]:
        """
        Download a Document file.

        Returns:
            A file as bytes.
        """

        url = self.session.server

        if role is None:
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.FILE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn, task=task_slug, role=role, resource=DownloadResource.FILE
            )

        response = requests.get(
            url=url,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        return response.content

    def download_images(
        self,
        task_slug: str,
        role: Optional[str] = None
    ) -> List[Tuple[str, bytes]]:
        """
        Download `Page` object images that can be used to complete the task.

        Returns:
            A list of tuples containing an image filename and bytes.

        # TODO include a list of `page_idx` values as an optional argument
          to filter images
        """

        url = self.session.server

        if role is None:
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.IMAGE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn, task=task_slug, role=role, resource=DownloadResource.IMAGE
            )

        response = requests.get(
            url=url,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        zipped = bytes_to_zipfile(response.content)
        return zipfile_to_byte_files(zipped)

    def download_service_file(
        self,
        task_slug: str,
        filename: str to be used, 
        role: Optional[str] = None
    ) -> bytes:
        """
        Download a service file related to this task, by providing its name.

        See `upload_service_file` for more information.

        Returns:
            A file as bytes.
        """

        url = self.session.server

        if role is None:
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.SERVICE_FILE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn, task=task_slug, role=role, resource=DownloadResource.SERVICE_FILE
            )

        response = requests.get(
            url=url,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        return response.content

    def upload_service_file(
        self,
        task_slug: str,
        filename: str to be used,
        file: bytes,
        role: Optional[str] = None
    ) -> None:
        """
        Upload a service file related to this task, by providing its name.

        A service file is a file that relates to a service and document,
          that can be used by the service to process a task through multiple steps
          the document relates to as the `Target` or an `Artefact` with a given role.

        Returns:
            None
        """

        url = self.session.server

        if role is None:
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.SERVICE_FILE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn, task=task_slug, role=role, resource=DownloadResource.SERVICE_FILE
            )

        files: Dict[str, Tuple[str, bytes]] = {
            "file": (filename, file),
        }

        response = requests.post(
            url=url,
            files=files,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        return None

    def download_pages(
        self,
        task_slug: str,
        role: Optional[str] = None
    ) -> List[Page]:
        """
        Download `Page` objects associated to a Document.

        Returns:
            A list of `Page` objects.

        # TODO include a list of `page_idx` values as an optional argument
          to filter pages
        """

        url = self.session.server

        if role is None:
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.PAGE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn, task=task_slug, role=role, resource=DownloadResource.PAGE
            )

        response = requests.get(
            url=url,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        document_metadata = response.json()

        return [Page.parse_obj(page) for page in document_metadata["result"]]

    def download_projections(
        self,
        task_slug: str,
        pkey: str, 
        role: Optional[str] = None
    ) -> List[Projection]:
        """
        Download `Projection` objects associated to a Document
          for a given projection key.

        Returns:
            A list of `Projection` objects.

        # TODO include a list of `xid` values as an optional argument
          to filter projections
        """

        url = self.session.server

        if role is None:
            url += ServiceUrl.TARGET_PROJECTION.format(
                provider=self.urn, task=task_slug, pkey=pkey, resource=DownloadResource.PROJECTION
            )
        else:
            url += ServiceUrl.ARTEFACT_PROJECTION.format(
                provider=self.urn, task=task_slug, role=role, pkey=pkey, resource=DownloadResource.PROJECTION
            )

        response = requests.get(
            url=url,
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        document_metadata = response.json()

        return [Projection.parse_obj(page) for page in document_metadata["result"]]
