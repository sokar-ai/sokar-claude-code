# 013 — Replace the update pipeline's Python tools with Sokar's shared tool

**Priority:** 1
**Opened:** 2026-09-13
**Source:** Sokar requirement B53, "The Build In One Language" - agent half handed to this repository on 2026-09-13; the operator made B53 first priority that day
**Depends on:** Sokar B53, which publishes the shared tool

## What

`update.yml` runs four Python files: `upstream-version.py`, `update.py`, `compare-bills.py` and
`check-pin.py`. The first two have already drifted between the three agent repositories; the bill
comparison has not. They are replaced by the tool Sokar publishes, with this agent's release
channel and download shape as configuration.

**`check-pin.py` is only half gone.** The version, the pom and the download URL agreeing is a unit
test now (`PinAgreementTest`). What remains is the one question a unit test cannot ask: whether the
pinned digest is the one Anthropic publishes. `build.yml` runs the script **on every push** for that
question, not only the update job - it is what catches a hand-made version bump that forgot the
digest, which builds, tests and packages green and fails only at an image build.

Whatever issue 004 settles about the update rules applies to the replacement unchanged.

## What would close it

- No `python3` left in `update.yml` or `build.yml`, and all four files deleted.
- **The digest check still runs on every push**, not only when the update job runs.
- Each replaced check **proven against the failure it exists for**, reproduced first: an older
  upstream than the pinned one stops red instead of rolling back; a digest that disagrees with the
  vendor's stops the update and fails a push; a bill that changed in a component the update did not
  name fails the comparison.
