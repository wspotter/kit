from app.modules.contract import validate_tool_definition


def test_tool_definition_requires_contract_fields():
    out = validate_tool_definition({"id": "x", "name": "X"})
    assert out.ok is False
    messages = "\n".join(i.message for i in out.issues)
    assert "Missing required TOOL_DEFINITION keys" in messages


def test_tool_definition_rejects_mock_true():
    td = {
        "id": "x",
        "name": "X",
        "description": "d",
        "version": "0.1.0",
        "ralph_loop": True,
        "allow_network": "none",
        "allow_filesystem": "none",
        "input_schema": {"type": "object", "properties": {}},
        "mock": True,
    }
    out = validate_tool_definition(td)
    assert out.ok is False
    assert any("mock tools are not allowed" in i.message for i in out.issues)
