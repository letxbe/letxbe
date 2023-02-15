from typing import List, Optional, Tuple, Union, cast

import requests

from letxbe.exception import AutomationError
from letxbe.provider.type import Page, ProjectionRoot
from letxbe.session import LXBSession
from letxbe.utils import bytes_to_zipfile, zipfile_to_byte_files

from .type import DownloadResource, LogStatus, SaverArgType, ServiceUrl, Task
from .utils import split_data_into_batches


class Provider(LXBSession):
    # TODO add documentation

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        provider_urn: str,
        server_address: Optional[str] = None,
    ) -> None:
        super(Provider, self).__init__(
            client_id=client_id,
            client_secret=client_secret,
            server_address=server_address,
        )
        self.__urn = provider_urn

    @property
    def urn(self) -> str:
        return self.__urn

    def _verify_response_is_success(self, res: requests.Response) -> None:
        self._verify_status_code(res)

        if "success" not in res.json():
            raise AutomationError(f"Error in response: {res}")
        return None

    def take_charge(
        self,
    ) -> Optional[Task]:
        """
        Take charge for the next task to be executed by the service provider.

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
        data: Tuple[
            SaverArgType
        ],  # TODO change this to Union[SaverArgType, Tuple[SaverArgType]]
        status_code: LogStatus = LogStatus.SUCCESS,
        text: str = "",
        exception: str = "",
    ) -> None:
        """
        Save data coming from a task and end the task to be executed by service.

        Remarks:
            Multiple saves can be made before finishing.

        Args:
            task_slug (str): the task slug
            data (Tuple[SaverArgType]): a tuple of SaverArgType objects to be saved
            status_code (LogStatus): status of the process outcome.
            text (str): a detailed log to store eventual warnings or errors.
            exception (str): a short exception to show on the front-end.

        Returns:
            Text of the HTTP response.
        """

        data_batches = split_data_into_batches(data)
        for batch in data_batches:
            if batch is None:
                # TODO update `split_data_into_batches` not to return None
                continue

            self._save(task_slug, batch)

        self._finish(
            task_slug=task_slug, status_code=status_code, text=text, exception=exception
        )
        return

    def _save(
        self,
        task_slug: str,
        data: Union[list, dict],
    ) -> None:

        res = requests.post(
            url=self.server + ServiceUrl.SAVE.format(provider=self.urn, task=task_slug),
            json=data,
            headers=self.authorization_header,
        )

        self._verify_response_is_success(res)
        return

    def _finish(
        self, task_slug: str, status_code: LogStatus, text: str, exception: str
    ) -> None:
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

    def download_document_file(
        self, task_slug: str, role: Optional[str] = None
    ) -> Tuple[str, bytes]:
        """
        Download the Document file associated to the task.

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
            # TODO change naming of TARGET_RESOURCE and ARTEFACT_RESOURCE as `role`
            #  not None does not mean that the document is a target or an artefact
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.FILE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn,
                task=task_slug,
                role=role,
                resource=DownloadResource.FILE,
            )

        res = requests.get(
            url=url,
            headers=self.authorization_header,
        )

        self._verify_response_is_success(res)

        # TODO develop and double check on web-service
        filename, filebytes = res.content
        return cast(str, filename), cast(bytes, filebytes)

    def download_images(
        self, task_slug: str, role: Optional[str] = None
    ) -> List[Tuple[str, bytes]]:
        """
        Download `Page` object images that can be used to complete the task.

        Returns:
            A list of tuples containing an image filename and bytes.

        # TODO include a list of `page_idx` values as an optional argument
          to filter images
        """

        url = self.server

        if role is None:
            # TODO change naming of TARGET_RESOURCE and ARTEFACT_RESOURCE as `role`
            #  not None does not mean that the document is a target or an artefact
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.IMAGE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
                provider=self.urn,
                task=task_slug,
                role=role,
                resource=DownloadResource.IMAGE,
            )

        res = requests.get(
            url=url,
            headers=self.authorization_header,
        )

        self._verify_response_is_success(res)

        zipped = bytes_to_zipfile(res.content)
        return zipfile_to_byte_files(zipped)

    def download_pages(self, task_slug: str, role: Optional[str] = None) -> List[Page]:
        """
        Download `Page` objects associated to a Document.

        Returns:
            A list of `Page` objects.

        # TODO include a list of `page_idx` values as an optional argument
          to filter pages
        """

        url = self.server

        if role is None:
            # TODO change naming of TARGET_RESOURCE and ARTEFACT_RESOURCE as `role`
            #  not None does not mean that the document is a target or an artefact
            url += ServiceUrl.TARGET_RESOURCE.format(
                provider=self.urn, task=task_slug, resource=DownloadResource.PAGE
            )
        else:
            url += ServiceUrl.ARTEFACT_RESOURCE.format(
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
        """
        Download `ProjectionRoot` objects associated to a Document
          for a given projection key.

        Returns:
            A list of `ProjectionRoot` objects.

        # TODO include a list of `xid` values as an optional argument
          to filter projections
        """

        url = self.server

        if role is None:
            url += ServiceUrl.TARGET_PROJECTION.format(
                provider=self.urn,
                task=task_slug,
                pkey=pkey,
                resource=DownloadResource.PROJECTION,
            )
        else:
            url += ServiceUrl.ARTEFACT_PROJECTION.format(
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
