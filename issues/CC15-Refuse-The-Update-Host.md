# CC15 — Refuse the update host once refusals are enforced

**Priority:** 3
**Opened:** 2026-09-18
**Source:** the operator saw Claude Code announce an update inside a task; answered in the channel
by the backend agent as QB14
**Depends on:** Sokar B61, which makes `refused_domains` reach the resolver

## What

`downloads.claude.ai` goes into `refused_domains` in `agent/claude.yaml`. The task needs nothing
from that host: the pinned binary is fetched when the package is built, not in the task.

The comment above `refused_domains` is corrected in the same change. It calls the entries "a
deliberate refusal", and until B61 nothing refuses them: the list reaches `sokar agents` and the
egress report, and neither the resolver nor the firewall.

## Why it is only a second line

The update itself is already stopped by `DISABLE_UPDATES=1` in the container's settings - see
"The CLI does not update itself in a task" in [`doc/decisions.md`](../doc/decisions.md). This issue
adds a network layer behind that, and a weak one:

- **Allowing `claude.ai` admits every name under it.** That is how the download got out, although
  `downloads.claude.ai` is not listed.
- **A refusal is by name, not by address.** Once B61 is built, the refused name does not resolve,
  but if it shares an address with an allowed host - usual behind a content delivery network - that
  address stays reachable.
- **Nothing finer than a host exists.** The egress is TLS and is not terminated, so a path such as
  `/claude-code-releases/` cannot be refused on its own.

## What would close it

- `downloads.claude.ai` listed in `refused_domains`, and the comment above the list saying what a
  refusal does and does not do.
- Measured in a task after B61: the name does not resolve, and the CLI still starts and works.
