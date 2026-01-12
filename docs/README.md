# Kit Docs

This folder is the home for developer-facing documentation.

## Current docs

- `MODULE_TUTORIAL.md` — how to create a backend tool module (contract + validator + example).

## How to write new tutorials (author checklist)

When you add a new tutorial, copy one of the templates below and fill it in.

Templates:
- `TEMPLATE_TUTORIAL.md` — generic tutorial template
- `TEMPLATE_INTEGRATION_TOOL.md` — template for writing a **real integration tool** tutorial (no mocks)

### Tutorial rules

- Keep it runnable: include exact commands and expected output.
- Prefer small, real examples over pseudo-code.
- Don’t introduce mock data or mock-only flows.
- Mention relevant files by path using backticks.
- Include a “Troubleshooting” section with 3–5 common failures.
- Include a quick verification checklist at the end.

## Naming convention

- Tutorials: `ALL_CAPS_WITH_UNDERSCORES.md` (consistent, easy to spot)
- Templates: `TEMPLATE_*.md`
