TOOL_DEFINITION = {
    "id": "inbox",
    "name": "Inbox Cleaner",
    "icon": "envelope",
    "description": "Inbox cleanup powered by the Ralph Loop (not implemented yet).",

    # Contract / governance
    "version": "0.1.0",
    "ralph_loop": True,
    "allow_network": "none",
    "allow_filesystem": "none",
    "input_schema": {
        "type": "object",
        "properties": {
            "dry_run": {"type": "boolean", "default": True},
        },
        "required": [],
        "additionalProperties": False,
    },
}


# Implementation of the Ralph Loop for Email
def clean_inbox():
    # 1. Observe
    # 2. Execute
    # 3. Verify
    # 4. Self-Correct
    pass


def run(payload: dict):
    # Placeholder runner used by /modules/run/inbox
    _ = payload
    return {"status": "noop", "message": "Inbox cleaner not implemented yet."}
