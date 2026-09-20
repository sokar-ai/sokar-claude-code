# CC07 — Drop `--dangerously-skip-permissions`

**Priority:** 3
**Opened:** 2026-09-13
**Source:** Sokar requirement B24, handed to this repository on 2026-09-13
**Depends on:** 006 in this repository

## What

`claude.yaml` declares `sandboxed.arguments: ["--dangerously-skip-permissions"]`. Measured
2026-09-10: `defaultMode: bypassPermissions` alone already puts the session in bypass mode - the
footer reads `⏵⏵ bypass permissions on` with and without the flag - and the flag is what raises the
bypass-mode warning. Dropping it removes the warning's cause rather than its symptom.

## What would close it

- The flag removed from `sandboxed.arguments`, and the comment there saying what now puts the
  session in bypass mode.
- Checked that Sokar accepts an agent that declares no sandboxed arguments at all, if that is what
  remains.
- The acceptance run still reaches work in bypass mode, attended and headless.
