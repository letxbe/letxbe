from enum import Enum


class DownloadResource(str, Enum):
    FILE = "file"
    PAGE = "page"
    PROJECTION = "projection"
    IMAGE = "image"
    SERVICE_FILE = "service_file"


class ServiceUrl(str, Enum):
    TASKS = "/api/provider/{provider:s}/task"
    SAVE = "/api/provider/{provider:s}/task/{task:s}/save"
    FINISH = "/api/provider/{provider:s}/task/{task:s}/finish"
    DOCUMENT = "/api/provider/{provider:s}/task/{task:s}/document"
    DOCUMENT_RESOURCE = "/api/provider/{provider:s}/task/{task:s}/resource/{resource:s}"
    DOCUMENT_PROJECTION = "/api/provider/{provider:s}/task/{task:s}/resource/{resource:s}/projection/{pkey:s}"
    ROLE = "/api/provider/{provider:s}/task/{task:s}/role/{role:s}/document"
    ROLE_RESOURCE = (
        "/api/provider/{provider:s}/task/{task:s}/role/{role:s}/resource/{resource:s}"
    )
    ROLE_PROJECTION = "/api/provider/{provider:s}/task/{task:s}/role/{role:s}/resource/{resource:s}/projection/{pkey:s}"


class LogStatus(str, Enum):
    """
    HOLD: process has been interrupted by the plateform or developer
    WAITING: some information is missing before process can start
    PROCESSING: a step is being processing
    """

    HOLD = "101"
    WAITING = "102"
    PROCESSING = "103"
    SUCCESS = "200"
    ERROR = "500"

    class Config:
        use_enum_values = True
