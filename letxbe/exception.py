class AuthorizationError(Exception):
    """Exception raised when a connection to the server is forbidden (403 Forbidden)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)


class UnkownRessourceError(Exception):
    """Exception raised when a requested ressource is not found (404 Not Found)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)


class AutomationError(Exception):
    """Exception raised when server is facing a internal error (500 Internal Server Error)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)
