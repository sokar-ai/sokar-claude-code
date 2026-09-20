# CC10 — Declare where this agent's session id is

**Priority:** 3
**Opened:** 2026-09-13
**Source:** Sokar requirement B46, agent half handed to this repository on 2026-09-13
**Depends on:** Sokar B46 - there is no manifest field to declare it in until B46 builds one. Also
the same issue in `sokar-pi` and `sokar-omp`, because the declaration should be one shape.

## What

A task that comes back should continue the conversation it was having. Sokar records the session id
and resumes with the declared `resume_flag`; where the id *is* is a fact about this agent, so this
package declares it, beside `supports_resume` and `resume_flag` in `claude.yaml`.

## What is claimed, not yet measured here

- **Headless:** the first `system` event carries the id of the session it opened (B46 names
  `session_id`). Note that `ClaudeStreamJsonFormatter` still drops exactly that event - the `init`
  line - which is right for a formatter. The declaration must not depend on what the formatter
  shows.
- **Attached:** the session files under the config directory, reportedly named after the id.

## What would close it

- Both routes measured on the pinned Claude Code version: the field in the headless event, and the
  location and naming of the session files of an attached run.
- The declaration in `claude.yaml`, in whatever shape B46 settles.
- A test that drives a short session and asserts the declared route still finds the id, so a
  version bump that moves it fails this build.

## Open question

Whether the headless id and the attached session file name are the same string - which decides
whether one declaration covers both modes.
