class UnauthorizedError(Exception):
    """Raised when a connection to the server is unauthorized (401 Unauthorized)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)


class ForbiddenError(Exception):
    """Raised when a connection to the server is forbidden (403 Forbidden)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)


class UnknownResourceError(Exception):
    """Raised when a requested resource is not found (404 Not Found)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)


class AutomationError(Exception):
    """Raised when server is facing an internal error (500 Internal Server Error)."""

    def __init__(self, error: str) -> None:
        super().__init__(error)
