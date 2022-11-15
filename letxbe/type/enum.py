from enum import Enum


class ClientEnv(str, Enum):
    PROD = "prod"
    TEST = "test"

    class Config:
        use_enum_values = True


class ActionCode(str, Enum):
    """
    Describe what a step does with a `Document`.

    PROJECTION: generate a representation (update document or projection field)
    PREDICTION: update prediction
    REPERCUSSION: apply an action externally
    """

    PROJECTION = "projection"
    PREDICTION = "prediction"
    REPERCUSSION = "repercussion"

    class Config:
        use_enum_values = True


class DocumentStatus(str, Enum):
    """
    HOLD: process has been interrupted by the plateform or developer
    WAITING: some information is missing before process can start
    PROCESSING: a step is being processing
    SUCCESS: step needs to be the last and log be `LogStatus.SUCCESS`
    ERROR: An error was encountered
    """

    HOLD = "101"
    WAITING = "102"
    PROCESSING = "103"
    SUCCESS = "200"
    ERROR = "500"

    class Config:
        use_enum_values = True


class FeedbackVote(str, Enum):
    VALID = "Valid"
    INVALID = "Invalid"

    class Config:
        use_enum_values = True


class Url(str, Enum):
    LOGIN = "/api/get_m2m_token"
    POST_DOCUMENT = "/api/automatisme/{automatisme_slug:s}/document"
    POST_ARTEFACT = "/api/automatisme/{automatisme_slug:s}/role/{role:s}/document"
    POST_FEEDBACK = (
        "/api/automatisme/{automatisme_slug:s}/document/{document_slug:s}/feedback"
    )
    GET_DOCUMENT = "/api/automatisme/{automatisme_slug:s}/document/{document_slug:s}"
