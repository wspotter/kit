# Kit Tool Modules — Dev Tutorial

This is the "how to add a tool" guide for Kit.

A **tool module** is a single Python file placed in `app/modules/` that:

1) **Describes itself** with `TOOL_DEFINITION` (a dict)
2) **Implements** a `run(payload: dict) -> Any` entrypoint
3) **Passes validation** (so it’s safe to discover & run)

If a module fails validation, it won’t be discoverable in `GET /modules/list` and it won’t be runnable via `POST /modules/run/{tool_id}`.

---

## 1) Required exports

### A) `TOOL_DEFINITION`

Kit expects these fields:

**Required keys**
- `id` (string) — unique tool id, used in URLs
- `name` (string) — display name
- `description` (string) — what the tool does
- `version` (string) — semver-ish (`"0.1.0"`)
- `ralph_loop` (boolean) — declare that this tool follows Observe → Execute → Verify → Self-Correct (max 3 tries)
- `allow_network` (`none|read|write`) — the tool’s *declared* network permission
- `allow_filesystem` (`none|read|write`) — the tool’s *declared* filesystem permission
- `input_schema` (dict) — lightweight JSON-schema-ish description of payload

**Optional keys**
- `icon` (string) — purely UI/presentation

### B) `run(payload: dict) -> Any`

- **Must exist** and be callable.
- Receives the JSON body from `POST /modules/run/{tool_id}` as a Python dict.
- Whatever it returns is placed in the API response under `result`.

---

## 2) The “no mockups” rule

Mock tools are rejected.

If your tool contains:

```python
TOOL_DEFINITION = {
  ...,
  "mock": True,
}
```

…it will fail validation and won’t load.

---

## 3) Input payload schema (quick guidance)

Kit doesn’t require a heavyweight schema dependency. The current contract expects a JSON-schema-ish dict.

A good minimum:

```python
"input_schema": {
  "type": "object",
  "properties": {
    "dry_run": {"type": "boolean", "default": True}
  },
  "required": [],
  "additionalProperties": False
}
```

Use `additionalProperties: False` whenever possible.

---

## 4) Safety declarations (what they mean)

`allow_network` and `allow_filesystem` are **declarations** used for safety review and gating.

Suggested interpretation:
- `none`: tool should not touch that resource category
- `read`: tool reads only (e.g., list emails, read files)
- `write`: tool may create/modify/delete (e.g., delete emails, move files)

Today, Kit uses these fields for validation and governance. (Future: we can enforce these more strictly with sandboxing or policy layers.)

---

## 5) Validate your tool

Run this from repo root:

```bash
python scripts/validate_tools.py
```

Typical output:
- `OK: app.modules.inbox_cleaner`
- `FAIL: app.modules.some_tool` plus error details

Exit codes:
- `0` all good
- `2` at least one tool failed

---

## 6) Minimal example tool (copy/paste)

Create `app/modules/hello_tool.py`:

```python
TOOL_DEFINITION = {
    "id": "hello",
    "name": "Hello Tool",
    "icon": "sparkles",
    "description": "Returns a greeting.",
    "version": "0.1.0",
    "ralph_loop": True,
    "allow_network": "none",
    "allow_filesystem": "none",
    "input_schema": {
        "type": "object",
        "properties": {
            "who": {"type": "string", "default": "world"},
        },
        "required": [],
        "additionalProperties": False,
    },
}


def run(payload: dict):
    who = payload.get("who") or "world"

    # Observe
    # Execute
    msg = f"Hello, {who}!"

    # Verify
    ok = isinstance(msg, str) and len(msg) > 0

    # Self-correct (tiny example)
    if not ok:
        msg = "Hello!"

    return {"status": "success", "message": msg}
```

Then validate:

```bash
python scripts/validate_tools.py
```

…and run it:

```bash
curl -s -X POST http://localhost:8000/modules/run/hello \
  -H 'content-type: application/json' \
  -d '{"who":"stacy"}' | jq
```

---

## 7) Checklist for PR reviews

A new tool should:
- [ ] Pass `python scripts/validate_tools.py`
- [ ] Declare minimal permissions (`allow_network`/`allow_filesystem`)
- [ ] Use `additionalProperties: False` unless there’s a good reason
- [ ] Follow the Ralph Loop (Observe/Execute/Verify/Self-correct) for side-effecting operations
- [ ] Have at least one pytest test around its core logic (especially verification criteria)
