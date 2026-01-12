from app.modules.registry import discover_tools


def test_discover_tools_includes_inbox():
    tools = {t.id for t in discover_tools()}
    assert "inbox" in tools
