from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class NormalizedAccount:
    source: str
    external_id: str
    username: str
    name: str
    url: str | None = None
    bio: str = ""
    followers: int = 0
    following: int = 0
    country: str | None = None
    language: str | None = None


@dataclass(frozen=True)
class NormalizedThread:
    source: str
    external_id: str
    account_external_id: str
    title: str
    body: str
    topic: str
    language: str | None = None
    post_count: int = 1
    likes: int = 0
    reposts: int = 0
    replies: int = 0
    created_at: datetime | None = None


class SourceAdapter(ABC):
    """Common contract implemented by every external source adapter."""

    key: str
    name: str

    @abstractmethod
    def search_accounts(self, query: str, limit: int = 20) -> list[NormalizedAccount]:
        """Return normalized public accounts matching a query."""
        raise NotImplementedError

    @abstractmethod
    def search_threads(self, query: str, limit: int = 20) -> list[NormalizedThread]:
        """Return normalized public content matching a query."""
        raise NotImplementedError

    def capabilities(self) -> dict[str, Any]:
        return {
            "search_accounts": True,
            "search_threads": True,
            "live_api": False,
        }
