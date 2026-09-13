# 013 — Replace the update pipeline's Python tools with Sokar's shared tool

**Priority:** 1
**Opened:** 2026-09-13
**Source:** Sokar requirement B53, "The Build In One Language" - agent half handed to this repository on 2026-09-13; the operator made B53 first priority that day
**Depends on:** Sokar B53, which publishes the shared tool

## What

`update.yml` runs four Python files: `upstream-version.py`, `update.py`, `check-pin.py` (for the
digest, the one question issue 011 cannot move) and `compare-bills.py`. The first two have already
drifted between the three agent repositories; the bill comparison has not. They are replaced by the
tool Sokar publishes, with this agent's release channel and download shape as configuration.

Whatever issue 004 settles about the update rules applies to the replacement unchanged.

## What would close it

- No `python3` left in `update.yml`, and all four files deleted.
- Each replaced check **proven against the failure it exists for**, reproduced first: an older
  upstream than the pinned one stops red instead of rolling back; a digest that disagrees with the
  vendor's stops the update; a bill that changed in a component the update did not name fails the
  comparison.
