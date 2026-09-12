# 002 — The stream formatter hides system events and malformed ones

**Priority:** 2
**Opened:** 2026-09-12
**Source:** `.codex-review.md`, finding C-06 (Low)

## What

`ClaudeStreamJsonFormatter` returns `null` for **every** `system` event, and also for an
`assistant` or `user` event whose `message.content` is missing or shaped unexpectedly. A `null`
line is dropped, so none of it reaches the operator.

## Why it matters

Only one system event is actually noise: the `init` line the CLI prints at startup, which is what
the current test pins. Everything else in that category - a warning, an error, a schema change
after an upstream version bump - disappears with it. The same holds for a recognized event the
formatter cannot parse: the run looks quieter than it is, exactly when somebody is trying to find
out why it failed.

This is the `task.log` an operator reads after an unattended run, so what is dropped here is not
recoverable from anywhere else.

## What would close it

- Suppress only the known benign event, matched by its subtype rather than by its category.
- Pass a recognized-but-malformed event through unchanged, with a visible marker saying it could
  not be parsed, rather than swallowing it.
- Tests for a system error, a system warning, and a malformed assistant event.

## Why it is not in the first round of fixes

It changes what an operator sees in every run, which is worth doing deliberately rather than
alongside a security batch. It was also missing from the grouping I put to the operator on
2026-09-12 - my oversight, recorded here so it is not lost a second time.
