# Kit: Project Rules
You are an expert developer building "Kit", an Atomic Era-themed AI assistant.

## Tech Stack
- Backend: Open WebUI (Headless) + FastAPI middleware.
- Frontend: React (Vite) + Tailwind CSS.
- Logic: "Ralph Loop" (Observe -> Execute -> Verify -> Self-Correct).

## Design Language (Atomic Era)
- Aesthetic: 1950s/60s advertising, Googie architecture.
- Colors: Teal (#008080), Tangerine (#FF8C00), Mustard (#E1AD01), Beige (#F1E4B7).
- Mascot: Minimalist mid-century black cat (animated during processing).

## Coding Standards
- Use the "Ralph Loop" pattern for all AI tools: verify the task was completed before returning a success message.
- Maintain a modular sidebar architecture where new modules can be dropped into `/app/modules/`.