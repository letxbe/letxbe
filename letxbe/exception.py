class AuthorizationError(Exception):
    def __init__(self, error: str) -> None:
        super().__init__(error)


class UnkownRessourceError(Exception):
    def __init__(self, error: str) -> None:
        super().__init__(error)


class AutomationError(Exception):
    def __init__(self, error: str) -> None:
        super().__init__(error)
