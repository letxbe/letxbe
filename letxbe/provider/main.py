from typing import List, Optional, Tuple, Union

import requests

from letxbe.exception import AutomationError
from letxbe.provider.type import Page, ProjectionRoot
from letxbe.session import LXBSession
from letxbe.utils import bytes_to_zipfile, zipfile_to_byte_files

from .type import DownloadResource, LogStatus, SaverArgType, ServiceUrl, Task
from .utils import split_data_into_batches


class Provider(LXBSession):
    # TODO add documentation

    # TODO Provider should not be initializated by its parent class
    def __init__(self, session: LXBSession, provider_urn: str):
        self.__session = session
        self.__urn = provider_urn

    @property
    def session(self) -> LXBSession:
        return self.__session

    @property
    def urn(self) -> str:
        return self.__urn

    def _verify_response(self, res: requests.Response) -> None:
        self.session._verify_status_code(res)

        if "success" not in res.json():
            raise AutomationError(f"Error in response: {res}")
        return None

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

    def save_and_finish(
        self,
        task_slug: str,
        data: Tuple[SaverArgType],
        status_code: LogStatus = LogStatus.SUCCESS,
        text: str = "",
        exception: str = "",
    ) -> None:
        # TODO change text and exception messages > they should be directly put in the Label
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
            url=self.session.server
            + ServiceUrl.SAVE.format(provider=self.urn, task=task_slug),
            json=data,
            headers=self.session.authorization_header,
        )

        self._verify_response(res)
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
            url=self.session.server
            + ServiceUrl.FINISH.format(provider=self.urn, task=task_slug),
            headers=self.session.authorization_header,
            data=data,
        )

        self._verify_response(res)
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

        url = self.session.server

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
            headers=self.session.authorization_header,
        )

        self._verify_response(res)

        # TODO add filename in output
        return "FILENAME-TO-BE-ADDED", res.content

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

        url = self.session.server

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
            headers=self.session.authorization_header,
        )

        self._verify_response(res)

        # TODO why?
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

        url = self.session.server

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
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

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

        url = self.session.server

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
            headers=self.session.authorization_header,
        )

        self.session._verify_status_code(response)

        document_metadata = response.json()

        return [ProjectionRoot.parse_obj(page) for page in document_metadata["result"]]

    # TODO add logic and documentation for service_file
    # def download_service_file(
    #     self,
    #     task_slug: str,
    #     filename: str to be used,
    #     role: Optional[str] = None
    # ) -> bytes:
    #     """
    #     Download a service file related to this task, by providing its name.
    #
    #     See `upload_service_file` for more information.
    #
    #     Returns:
    #         A file as bytes.
    #     """
    #
    #     url = self.session.server
    #
    #     if role is None:
    #         url += ServiceUrl.TARGET_RESOURCE.format(
    #             provider=self.urn, task=task_slug, resource=DownloadResource.SERVICE_FILE
    #         )
    #     else:
    #         url += ServiceUrl.ARTEFACT_RESOURCE.format(
    #             provider=self.urn, task=task_slug, role=role, resource=DownloadResource.SERVICE_FILE
    #         )
    #
    #     response = requests.get(
    #         url=url,
    #         headers=self.session.authorization_header,
    #     )
    #
    #     self.session._verify_status_code(response)
    #
    #     return response.content
    #
    # def upload_service_file(
    #     self,
    #     task_slug: str,
    #     filename: str to be used,
    #     file: bytes,
    #     role: Optional[str] = None
    # ) -> None:
    #     """
    #     Upload a service file related to this task, by providing its name.
    #
    #     A service file is a file that relates to a service and document,
    #       that can be used by the service to process a task through multiple steps
    #       the document relates to as the `Target` or an `Artefact` with a given role.
    #
    #     Returns:
    #         None
    #     """
    #
    #     url = self.session.server
    #
    #     if role is None:
    #         url += ServiceUrl.TARGET_RESOURCE.format(
    #             provider=self.urn, task=task_slug, resource=DownloadResource.SERVICE_FILE
    #         )
    #     else:
    #         url += ServiceUrl.ARTEFACT_RESOURCE.format(
    #             provider=self.urn, task=task_slug, role=role, resource=DownloadResource.SERVICE_FILE
    #         )
    #
    #     files: Dict[str, Tuple[str, bytes]] = {
    #         "file": (filename, file),
    #     }
    #
    #     response = requests.post(
    #         url=url,
    #         files=files,
    #         headers=self.session.authorization_header,
    #     )
    #
    #     self.session._verify_status_code(response)
    #
    #     return None
