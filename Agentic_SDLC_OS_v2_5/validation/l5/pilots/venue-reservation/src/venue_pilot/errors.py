from __future__ import annotations


class DomainError(RuntimeError):
    def __init__(self, code: str, message: str, status_code: int = 400, *, next_action: str = "Review the request and retry.") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.next_action = next_action
