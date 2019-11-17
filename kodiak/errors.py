from dataclasses import dataclass
from typing import List, Set
from starlette import status
from fastapi import HTTPException

from requests_async import Response


class KodiakException(Exception):
    """
    base Kodiak Exception to make catching all Kodiak related exceptions
    easier
    """


class Queueable(KodiakException):
    pass


class MissingGithubMergeabilityState(KodiakException):
    """Github hasn't evaluated if this PR can be merged without conflicts yet"""


class NeedsBranchUpdate(KodiakException):
    pass


class WaitingForChecks(KodiakException):
    def __init__(self, checks: Set[str]):
        self.checks = checks
        super().__init__()


class NotQueueable(KodiakException):
    pass


class MissingSkippableChecks(KodiakException):
    def __init__(self, checks: List[str]):
        self.checks = checks
        super().__init__()


class MergeBlocked(KodiakException):
    pass


class MissingAppID(KodiakException):
    """
    Application app_id doesn't match configuration

    We do _not_ want to display this message to users as it could clobber
    another instance of kodiak.
    """

    def __str__(self) -> str:
        return "missing Github app id"


class BranchMerged(KodiakException):
    """branch has already been merged"""

    def __str__(self) -> str:
        return str(self.__doc__)


class MergeConflict(KodiakException):
    """Merge conflict in the PR."""

    def __str__(self) -> str:
        return "merge conflict"


class HTTPBadRequest(KodiakException, HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
