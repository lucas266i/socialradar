from .base import SourceAdapter
from .stub import StubAdapter


_ADAPTERS: dict[str, SourceAdapter] = {
    "x": StubAdapter("x", "X"),
    "reddit": StubAdapter("reddit", "Reddit"),
    "youtube": StubAdapter("youtube", "YouTube"),
    "github": StubAdapter("github", "GitHub"),
}


def get_adapter(source_key: str) -> SourceAdapter | None:
    return _ADAPTERS.get(source_key.strip().lower())


def list_adapters() -> list[SourceAdapter]:
    return list(_ADAPTERS.values())
