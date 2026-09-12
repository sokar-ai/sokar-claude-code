# 005 — Declare what waiting looks like for this agent

**Priority:** 2
**Opened:** 2026-09-12
**Source:** handed over from Sokar requirement **A11**, 2026-09-12, which I wrote and measured.
The requirement covered all three agents; this is this repository's share.
**Depends on:** Sokar requirement **B47** (the daemon side: the manifest field, the matcher, the
contract). Nothing here can be read by anything until that exists. It also depends on the same
issue in `sokar-pi` and `sokar-omp`, because the declaration's shape should be one shape.

## What this agent has to declare

Both halves. This agent's attached screen is the richest of the three: a status line that says
`esc to interrupt` while it works, a numbered list with `Enter to select · ↑/↓ to navigate · Esc to
cancel` when it asks, and `Enter to confirm · Esc to cancel` for the first-run consents.

## What is already known, measured 2026-09-12

- **Headless: nothing to declare.** Asked to put a question to the person and wait, it asks and
  then *ends the run* - `stop_reason=end_turn`, `terminal_reason=completed`. Nothing distinguishes
  a run that ended by asking from one that ended by finishing.
- **Attached: `Esc to cancel` is the one literal that separates waiting from both other states**,
  and both markers vanish the moment the question is answered.
- **The window title is useless here**: `✳ Claude Code`, then `✳ <what the task is about>`,
  unchanged across working, waiting and idle.

## What would close it

- A declaration in `src/main/resources/agent/claude.yaml`, written from a measurement rather than from
  upstream's documentation.
- A test in this repository that drives the agent to a waiting point and asserts the declaration
  still matches - so a version bump that changes the wording fails this build instead of going
  quiet in the field.
- Or, where there is nothing to declare, a test asserting the contract reports *cannot say* rather
  than *not waiting*.

## Why it waits on B47

The manifest field does not exist yet, and the reader for it does not exist yet. A declaration
written now would be text nothing parses. What can be done before B47 lands is the measurement,
and that is done.
