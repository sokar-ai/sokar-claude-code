# CC06 — Find out which setting silences the bypass-mode warning

**Priority:** 2
**Opened:** 2026-09-13
**Source:** Sokar requirement B24, handed to this repository on 2026-09-13

## What

`ClaudeSettings` writes two keys: `permissions.defaultMode: bypassPermissions` and
`skipDangerousModePermissionPrompt: true`. With both in place the *"Bypass Permissions mode"*
warning does not appear (measured 2026-09-10). Those runs cannot say which key does it.

## Why it matters

CC07 removes the flag that raises the warning. That removal should rest on knowing which key
holds the mode and which silences the dialog, not on both happening to be present. A key that turns
out to do nothing is a line nobody can later explain.

## What would close it

- One run with only `defaultMode`, one with only `skipDangerousModePermissionPrompt`, each with and
  without `--dangerously-skip-permissions`, at a real terminal in `/workspace` on a machine where
  the agent never ran.
- The result in `ClaudeSettings`' comments, and a key that does nothing removed - or both kept with
  the measured reason.
