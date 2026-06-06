# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — shared/system-wide glossary covering concepts that span both backend and frontend.
- **`CONTEXT-MAP.md`** at the repo root — points at per-context `CONTEXT.md` files. Read each one relevant to the topic.
  - `backend/CONTEXT.md` — backend-specific domain terms
  - `frontend/CONTEXT.md` — frontend-specific domain terms
- **`docs/adr/`** — read ADRs that touch the area you're about to work in.
- Also check `backend/docs/adr/` and `frontend/docs/adr/` for context-scoped decisions if they exist.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved.

## File structure

```
/
├── CONTEXT.md          ← shared/system-wide glossary
├── CONTEXT-MAP.md      ← index of per-context files
├── docs/adr/           ← system-wide architectural decisions
├── backend/
│   ├── CONTEXT.md      ← backend domain terms
│   └── docs/adr/       ← backend-specific decisions
└── frontend/
    ├── CONTEXT.md      ← frontend domain terms
    └── docs/adr/       ← frontend-specific decisions
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in the relevant `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
