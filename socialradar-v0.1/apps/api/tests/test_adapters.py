from app.adapters import get_adapter, list_adapters


def test_default_adapters_are_registered():
    keys = {adapter.key for adapter in list_adapters()}
    assert keys == {"x", "reddit", "youtube", "github"}


def test_unknown_adapter_returns_none():
    assert get_adapter("unknown") is None


def test_adapter_is_case_insensitive():
    assert get_adapter(" X ").key == "x"


def test_stub_adapter_has_no_live_api():
    adapter = get_adapter("github")
    assert adapter is not None
    assert adapter.capabilities()["live_api"] is False
    assert adapter.search_accounts("test") == []
    assert adapter.search_threads("test") == []
