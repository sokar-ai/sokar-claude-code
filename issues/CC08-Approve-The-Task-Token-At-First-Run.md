# CC08 — Approve the task's own token so the API-key dialog never asks

**Priority:** 1
**Opened:** 2026-09-13
**Source:** Sokar requirement B24, handed to this repository on 2026-09-13

## What

Started with a token in its environment, Claude Code opens with *"Detected a custom API key in your
environment - Do you want to use this API key?"* and recommends **No**. The key it shows is the
phantom token Sokar minted for this task. Unattended, nobody answers and the task waits at a menu.
Attended, taking the recommendation refuses the only credential the task has.

## Decided

Suppress it - operator, 2026-09-13. The reasoning, and why the refusal of 2026-09-09 no longer
holds, is in [`doc/decisions.md`](../doc/decisions.md).

## Already measured

Listing the last 20 characters of the token under `customApiKeyResponses.approved` in
`/home/agent/.claude.json` removes the dialog completely - Claude Code 2.1.267, in a task container
on the ubuntu VM, 2026-09-10.

## What would close it

- `ClaudeFirstRun` writes the approval when the task has a token, and no approval when the token is
  empty.
- A unit test for both shapes, run against the unchanged class first.
- Measured at a real terminal in `/workspace`, on a machine where the agent never ran: with a token,
  the CLI reaches its prompt with no dialog.
- The same headless: a run with a token completes instead of waiting.
