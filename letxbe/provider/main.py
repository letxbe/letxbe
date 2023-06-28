import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import requests
from PIL.Image import Image

from letxbe.exception import AutomationError
from letxbe.provider.type import (
    DownloadResource,
    LogStatus,
    Page,
    ProjectionRoot,
    SaverArgType,
    ServiceUrl,
    Task,
    UploadResource,
)
from letxbe.provider.type.page import ImageFormat
from letxbe.session import LXBSession
from letxbe.utils import (
    bytes_to_zipfile,
    extract_filename_from_response_header,
    pil_image_to_bytes,
    pydantic_model_to_json,
    zip_files,
    zipfile_to_byte_files,
)


class Provider(LXBSession):
    """
    A Provider is a third-party that contributes to processing documents with their own algorithms.
    This object allows them to load a pending document and resources available to process it.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        provider_urn: str,
        server_address: Optional[str] = None,
    ) -> None:
        """
        Args:
            Args:
            client_id (str): Auth0 client ID.
            client_secret (str): Auth0 client secret.
            provider_urn (str):
            server_address (str): Address of the server.
        """
        super(Provider, self).__init__(
            client_id=client_id,
            client_secret=client_secret,
            server_address=server_address,
        )
        self.__urn = provider_urn

    @property
    def urn(self) -> str:
        """URN of the provider"""
        return self.__urn

    def _verify_response_is_success(self, res: requests.Response) -> None:
        """
        Args:
            res (requests.Response):

        Raises:
            AutomationError: If the server is facing a internal error (500 Internal Server Error).
        """
        self._verify_status_code(res)

        if "success" not in res.json():
            raise AutomationError(f"Error in response: {res}")
        return None

    def take_charge(
        self,
    ) -> Optional[Task]:
        """Take charge for the next task to be executed by the service provider.

        Returns:
            A Task object.
        """
        response = requests.post(
            url=self.server + ServiceUrl.TASKS.format(provider=self.urn),
            headers=self.authorization_header,
        )
        self._verify_status_code(response)

        response_json = response.json()
        if response_json == {}:
            return None

        return Task.parse_obj(response_json)

    def save_and_finish(
        self,
        task_slug: str,
        data: Optional[Union[SaverArgType, Tuple[SaverArgType]]],
        status_code: LogStatus = LogStatus.SUCCESS,
        text: str = "",
        exception: str = "",
    ) -> None:
        """Save data coming from a task and end the task to be executed by service.

        Args:
            task_slug (str): the task slug
            data (Tuple[SaverArgType]): a tuple of SaverArgType objects to be saved
            status_code (LogStatus): status of the process outcome.
            text (str): a detailed log to store eventual warnings or errors.
            exception (str): a short exception to show on the front-end.

        Returns:
            Text of the HTTP response.

        Remarks:
            Multiple saves can be made before finishing.
        """
        if data is not None:
            self._save(task_slug, data)

        self._finish(
            task_slug=task_slug, status_code=status_code, text=text, exception=exception
        )
        return

    def _save(
        self,
        task_slug: str,
        data: Union[SaverArgType, Tuple[SaverArgType]],
    ) -> None:
        """
        Args:
            task_slug (str):
            data (Union[SaverArgType, Tuple[SaverArgType]]):
        """

        to_save: List[Union[Dict, List[Dict]]] = []

        if isinstance(data, tuple):
            tuppled_data = data
        else:
            tuppled_data = (data,)

        content_header = {"Content-Type": "application/json"}
        if len(tuppled_data) > 1 and any(
            isinstance(element, bytes) for element in tuppled_data
        ):
            raise NotImplementedError

        for vec in tuppled_data:
            if isinstance(vec, bytes):
                content_header = {"Content-Type": "application/octet-stream"}
                self._send_request(vec, task_slug, content_header)
                return
            if isinstance(vec, list):
                to_save += [[pydantic_model_to_json(element) for element in vec]]
                continue
            to_save += [pydantic_model_to_json(vec)]
        self._send_request(to_save, task_slug, content_header)
        return

    def _send_request(
        self,
        to_save: Union[bytes, List[Union[Dict, List[Dict]]]],
        task_slug: str,
        content_header: Dict[str, str],
    ) -> None:
        """
        Args:
            to_save (Union[bytes, List[Union[Dict, List[Dict]]]]):
            task_slug (str):
            content_header (Dict[str, str]):
        """
        res = requests.post(
            url=self.server + ServiceUrl.SAVE.format(provider=self.urn, task=task_slug),
            json=to_save,
            headers={**self.authorization_header, **content_header},
        )

        self._verify_response_is_success(res)
        return

    def _finish(
        self, task_slug: str, status_code: LogStatus, text: str, exception: str
    ) -> None:
        """
        Args:
            task_slug (str):
            status_code (LogStatus):
            text (str):
            exception (str):
        """
        data = {
            "status_code": status_code.value,
            "text": text,
            "exception": exception,
        }

        res = requests.post(
            url=self.server
            + ServiceUrl.FINISH.format(provider=self.urn, task=task_slug),
            headers=self.authorization_header,
            data=data,
        )

        self._verify_response_is_success(res)
        return

    def properties(self, task_slug: str) -> Dict[str, Any]:
        """
        Args:
            task_slug (str):

        Returns:
            Dict[str, Any]:
        """
        res = requests.get(
            url=self.server
            + ServiceUrl.DOCUMENT.format(provider=self.urn, task=task_slug),
            headers=self.authorization_header,
        )

        return cast(dict, res.json())

    def upload_images(
        self,
        task_slug: str,
        images: List[Image],
        image_fmt: ImageFormat,
        batch: int = 0,
    ) -> None:
        """
        Upload images to S3.

        Args:
            task_slug (str): Slug of the task being treated.
            images (List[Images]): Images to upload.
            image_fmt (ImageFormat): Format of the images.
            batch (int, default 0): If uploading images by batches, indicate the value
                of batch to avoid overwriting images.
        """
        tupled_images = [
            (f"{task_slug}_{k + batch}", pil_image_to_bytes(image))
            for k, image in enumerate(images)
        ]
        zipped_images = zip_files(tupled_images)
        files = {"file": zipped_images}
        res = requests.post(
            url=self.server
            + ServiceUrl.DOCUMENT_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=UploadResource.IMAGE
            ),
            headers=self.authorization_header,
            files=files,
            params={"format": image_fmt, "offset": batch},  # type: ignore[arg-type]
        )

        self._verify_response_is_success(res)
        return

    def upload_pages(self, task_slug: str, pages: List[Page]) -> None:
        """
        Args:
            task_slug (str):
            pages (List[Page]):
        """
        json_pages = [pydantic_model_to_json(page) for page in pages]
        res = requests.post(
            url=self.server
            + ServiceUrl.DOCUMENT_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=UploadResource.PAGE
            ),
            headers=self.authorization_header,
            data=json.dumps({"pages": json_pages}),
        )

        self._verify_response_is_success(res)
        return

    def download_document_file(
        self, task_slug: str, role: Optional[str] = None
    ) -> Tuple[Optional[str], bytes]:
        """Download the Document file associated to the task.

        By default, the document concerned by the task is downloaded. If `role` is
        not None, then the document attached to the task via `role` is downloaded.

        Args:
            task_slug (str): the task slug
            role (str, None): default None, if present the document with the given role
                is downloaded.

        Returns:
            A tuple containing the filename (str) and the file (bytes).
        """

        url = self.server

        if role is None:
            url += ServiceUrl.DOCUMENT_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.FILE
            )
        else:
            url += ServiceUrl.ROLE_RESOURCE.format(
                provider=self.urn,
                task=task_slug,
                role=role,
                resource=DownloadResource.FILE,
            )

        res = requests.get(
            url=url,
            headers=self.authorization_header,
        )

        try:
            fname = extract_filename_from_response_header(res)
            return fname, cast(bytes, res.content)
        except (ValueError, KeyError, IndexError):
            return None, cast(bytes, res.content)

    def download_images(
        self, task_slug: str, role: Optional[str] = None
    ) -> List[Tuple[str, bytes]]:
        """Download `Page` object images that can be used to complete the task.

        Returns:
            A list of tuples containing an image filename and bytes.

        Todo:
            Iinclude a list of `page_idx` values as an optional argument
            to filter images
        """

        url = self.server

        if role is None:
            url += ServiceUrl.DOCUMENT_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.IMAGE
            )
        else:
            url += ServiceUrl.ROLE_RESOURCE.format(
                provider=self.urn,
                task=task_slug,
                role=role,
                resource=DownloadResource.IMAGE,
            )

        res = requests.get(
            url=url,
            headers=self.authorization_header,
        )

        self._verify_status_code(res)

        zipped = bytes_to_zipfile(res.content)
        return zipfile_to_byte_files(zipped)

    def download_pages(self, task_slug: str, role: Optional[str] = None) -> List[Page]:
        """Download `Page` objects associated to a Document.

        Returns:
            A list of `Page` objects.

        Todo: include a list of `page_idx` values as an optional argument
            to filter pages
        """

        url = self.server

        if role is None:
            url += ServiceUrl.DOCUMENT_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.PAGE
            )
        else:
            url += ServiceUrl.ROLE_RESOURCE.format(
                provider=self.urn,
                task=task_slug,
                role=role,
                resource=DownloadResource.PAGE,
            )

        response = requests.get(
            url=url,
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        document_metadata = response.json()

        return [Page.parse_obj(page) for page in document_metadata["result"]]

    def download_projections(
        self, task_slug: str, pkey: str, role: Optional[str] = None
    ) -> List[ProjectionRoot]:
        """Download `ProjectionRoot` objects associated to a Document
        for a given projection key.

        Returns:
            A list of `ProjectionRoot` objects.

        Todo: include a list of `xid` values as an optional argument
            to filter projections
        """

        url = self.server

        if role is None:
            url += ServiceUrl.DOCUMENT_PROJECTION.format(
                provider=self.urn,
                task=task_slug,
                pkey=pkey,
                resource=DownloadResource.PROJECTION,
            )
        else:
            url += ServiceUrl.ROLE_PROJECTION.format(
                provider=self.urn,
                task=task_slug,
                role=role,
                pkey=pkey,
                resource=DownloadResource.PROJECTION,
            )

        response = requests.get(
            url=url,
            headers=self.authorization_header,
        )

        self._verify_status_code(response)

        document_metadata = response.json()

        return [ProjectionRoot.parse_obj(page) for page in document_metadata["result"]]
