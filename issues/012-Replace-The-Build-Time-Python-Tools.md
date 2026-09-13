# 012 — Replace the build-time Python tool with Sokar's shared tool

**Priority:** 1
**Opened:** 2026-09-13
**Source:** Sokar requirement B53, "The Build In One Language" - agent half handed to this repository on 2026-09-13; the operator made B53 first priority that day
**Depends on:** Sokar B53, which publishes the shared tool

## What

`add-fetched-cli.py` runs on every package build, from the `exec-maven-plugin` in `pom.xml`. It is
replaced by the tool Sokar publishes, with this agent's difference as configuration rather than a
copy.

The changelog check that stood beside it here is gone rather than replaced: removed on 2026-09-13 by
the operator's decision. Requiring an entry returns with Sokar B55, built on logchange - the
reasoning is in [`doc/decisions.md`](../doc/decisions.md).

## What would close it

- The call replaced; no `python3` left in `pom.xml`.
- The replaced check **proven against the failure it exists for**, reproduced before the Python file
  is deleted - whatever `add-fetched-cli.py`'s own header says it guards, reproduced from that header
  rather than from memory.
- The Python file deleted.
