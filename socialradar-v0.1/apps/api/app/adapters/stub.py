from .base import NormalizedAccount, NormalizedThread, SourceAdapter


class StubAdapter(SourceAdapter):
    """Safe placeholder until an official/public source API is configured."""

    def __init__(self, key: str, name: str):
        self.key = key
        self.name = name

    def search_accounts(self, query: str, limit: int = 20) -> list[NormalizedAccount]:
        return []

    def search_threads(self, query: str, limit: int = 20) -> list[NormalizedThread]:
        return []
