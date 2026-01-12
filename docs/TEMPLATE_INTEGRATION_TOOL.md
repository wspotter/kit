# <INTEGRATION TOOL NAME> — Tutorial

> Audience: devs implementing **real** tool integrations for Kit (no mocks).
>
> Goal: add a new tool under `app/modules/` that passes validation and can be run safely.

## Tool checklist (must-haves)

- [ ] Tool passes `python scripts/validate_tools.py`
- [ ] Tool follows the Ralph Loop (observe → execute → verify → self-correct, max 3)
- [ ] Tool declares minimal permissions:
  - `allow_network`: `none|read|write`
  - `allow_filesystem`: `none|read|write`
- [ ] Tool supports `dry_run` when it can write/delete/mutate
- [ ] Tool has at least 1 pytest test covering verification logic
- [ ] Tool does not embed secrets; uses env vars

## 1) Decide the integration surface

Write down:
- **External system:** <API/IMAP/filesystem/etc>
- **Auth method:** <env vars/keys/oauth/etc>
- **Rate limits:** <what’s safe>
- **Idempotency key:** <how we avoid duplicate side effects>

## 2) Define the contract (`TOOL_DEFINITION`)

Start from the required keys:

```python
TOOL_DEFINITION = {
  "id": "<id>",
  "name": "<Name>",
  "icon": "tool",
  "description": "<what it does>",
  "version": "0.1.0",
  "ralph_loop": True,
  "allow_network": "<none|read|write>",
  "allow_filesystem": "<none|read|write>",
  "input_schema": {
    "type": "object",
    "properties": {
      "dry_run": {"type": "boolean", "default": True}
    },
    "required": [],
    "additionalProperties": False
  }
}
```

Rules:
- Use `additionalProperties: False` unless you have a strong reason.
- If the tool can mutate state, include `dry_run`.

## 3) Implement `run(payload)` with the Ralph Loop

Structure:
- Observe: fetch current state
- Execute: perform the action (or simulate if `dry_run`)
- Verify: re-fetch state / compare
- Self-correct: adjust + retry up to 3

Guidelines:
- Keep retries bounded and explicit.
- Return a `trace` array (steps + notes) so the UI can show what happened.
- Never log secrets.

## 4) Add tests

At minimum:
- verifies the verification condition correctly detects success and failure
- tests `dry_run` does not mutate external state

## 5) Validate + run

```bash
python scripts/validate_tools.py
pytest -q
```

Then run via API:

```bash
curl -s -X POST http://localhost:8000/modules/run/<id> \
  -H 'content-type: application/json' \
  -d '{"dry_run": true}'
```

## Troubleshooting

- **Validator fails with missing keys**
  - Add contract fields to `TOOL_DEFINITION`.

- **Tool imports fail**
  - Avoid importing optional heavy dependencies at module import time.
  - Move them inside `run()` if possible, and add dependencies explicitly.

- **Side effects happen unexpectedly**
  - Ensure `dry_run` is the default.
  - Ensure the execute step is gated behind `dry_run == False`.
