from enum import Enum


class ClientEnv(str, Enum):
    """Describe the environment in which a `Document` will be sent:

    - PROD: production environment
    - TEST: test environment
    """

    PROD = "prod"
    TEST = "test"

    class Config:
        use_enum_values = True


class ActionCode(str, Enum):
    """Describe what kind of processing step is applied to a `Document`:

    - PROJECTION: generate a representation (update document or projection field)
    - PREDICTION: update prediction
    - REPERCUSSION: apply an action externally
    """

    PROJECTION = "projection"
    PREDICTION = "prediction"
    REPERCUSSION = "repercussion"

    class Config:
        use_enum_values = True


class DocumentStatus(str, Enum):
    """Describe the status of a `Document` processing step:

    - HOLD: Process has been interrupted by the plateform or developer
    - WAITING: Some information is missing before process can start
    - PROCESSING: A step is being processing
    - SUCCESS: Step needs to be the last and log be `LogStatus.SUCCESS`
    - ERROR: An error was encountered
    """

    HOLD = "101"
    WAITING = "102"
    PROCESSING = "103"
    SUCCESS = "200"
    ERROR = "500"

    class Config:
        use_enum_values = True


class FeedbackVote(str, Enum):
    """Describe the value of a `Label` as:

    - VALID:
    - INVALID:
    """

    VALID = "Valid"
    INVALID = "Invalid"

    class Config:
        use_enum_values = True


class Url(str, Enum):
    """URLs used for requests:

    - LOGIN: Connection to LetXBe. Returns an acces token.
    - POST_DOCUMENT: Post a document. Returns the document slug.
    - POST_ARTEFACT: Post an artefact. Returns the dpcument slug.
    - POST_PREDICTION: Post a prediction on a given document slug.
    - GET_DOCUMENT: Request a document associated on a given document slug.
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
