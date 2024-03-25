from enum import Enum


class ClientEnv(str, Enum):
    """
    Describe the environment in which a `Document`_ is sent to.

    Attributes:
        PROD: Production environment.
        TEST: Test environment.
    """

    PROD = "prod"
    TEST = "test"


class ActionCode(str, Enum):
    """
    Processing step applied to a `Document`_.

    Attributes:
        PROJECTION: The document is read and interpreted, its content is saved in the database.
        PREDICTION: The document has been treated and the prediction is available.
        REPERCUSSION: An (external) action has been triggered.

    Todo:
        Change PROJECTION to READING.
    """

    PROJECTION = "projection"
    PREDICTION = "prediction"
    REPERCUSSION = "repercussion"


class DocumentStatus(str, Enum):
    """Status of a `Document`_.

    Attributes:
        HOLD: Process has been interrupted by the platform or developer.
        WAITING: Some information is missing before the process can start.
        PROCESSING: A step is being processed.
        SUCCESS: The step has been correctly applied.
        ERROR: An error has occurred.
    """

    HOLD = "101"
    WAITING = "102"
    PROCESSING = "103"
    SUCCESS = "200"
    ERROR = "500"


class FeedbackVote(str, Enum):
    """Vote choices in a `LabelFeedback`_.

    Attributes:
        VALID: The prediction has been validated.
        INVALID: The prediction has been invalidated.
    """

    VALID = "Valid"
    INVALID = "Invalid"


class Url(str, Enum):
    """URLs used for requests.

    Attributes:
        LOGIN: Connection to LetXBe. Returns an acces token.
        POST_DOCUMENT: Post a document. Returns the document slug.
        POST_ARTEFACT: Post an artefact. Returns the document slug.
        POST_PREDICTION: Post a prediction on a given document slug.
        GET_DOCUMENT: Request a document associated on a given document slug.
    """

    LOGIN = "/api/get_m2m_token"
    POST_DOCUMENT = "/api/automatisme/{automatisme_slug:s}/document"
    POST_ARTEFACT = "/api/automatisme/{automatisme_slug:s}/role/{role:s}/document"
    POST_FEEDBACK = (
        "/api/automatisme/{automatisme_slug:s}/document/{document_slug:s}/feedback"
    )
    POST_PREDICTION = (
        "/api/automatisme/{automatisme_slug:s}/document/{document_slug:s}/prediction"
    )
    GET_DOCUMENT = "/api/automatisme/{automatisme_slug:s}/document/{document_slug:s}"


class ServiceUrl(str, Enum):
    """
    Attributes:
        TASK:
        SAVE:
        FINISH:
        TARGET:
        TARGET_RESOURCE:
        TARGET_PROJECTION:
        ARTEFACT:
        ARTEFACT_RESOURCE:
        ARTEFACT_PROJECTION:

    Todo:
        Add documentation
    """

    TASKS = "/api/service/{service:s}/task"
    SAVE = "/api/service/{service:s}/task/{task:s}/save"
    FINISH = "/api/service/{service:s}/task/{task:s}/finish"
    TARGET = "/api/service/{service:s}/task/{task:s}/document"
    TARGET_RESOURCE = "/api/service/{service:s}/task/{task:s}/resource/{resource:s}"
    TARGET_PROJECTION = "/api/service/{service:s}/task/{task:s}/resource/{resource:s}/projection/{pkey:s}"
    ARTEFACT = "/api/service/{service:s}/task/{task:s}/role/{role:s}/document"
    ARTEFACT_RESOURCE = (
        "/api/service/{service:s}/task/{task:s}/role/{role:s}/resource/{resource:s}"
    )
    ARTEFACT_PROJECTION = "/api/service/{service:s}/task/{task:s}/role/{role:s}/resource/{resource:s}/projection/{pkey:s}"
