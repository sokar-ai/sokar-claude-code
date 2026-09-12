# Decisions

Settled reasoning that outlives the change that produced it. A decision is written here when
somebody would otherwise ask "why is it like this?" and find only code.

Accepted risks live here too. An accepted risk is not a forgotten one: it says what the exposure
is, why it is not being removed, and what would change the answer.

## Accepted risk: the release binary and its digest share one trust root

**Decided:** 2026-09-12, from the security review in `.codex-review.md` (C-04).

This package installs Claude Code from `downloads.claude.ai`, pinned to a version and checked
against a SHA-256 recorded in `agent/claude.yaml`. The digest that pin is compared with comes from
`manifest.json` on **the same service**.

That protects against a corrupted or partial download, a mismatched pin and an accidental version
drift. It does **not** prove authenticity: anybody who can change both objects - a compromised CDN,
release account, publication path or TLS termination - passes every check this repository makes.

**Why it is accepted rather than fixed:** the vendor publishes no signature, attestation or
independent digest source that we could verify against. A check we cannot perform cannot be
written. The alternative - refusing to ship the agent at all - removes a product rather than a
risk.

**What would change it:** a signed release, a provenance attestation, or a digest published
through a channel with a different operator. Any of those should be verified in the update job and
recorded in the bill of materials.

**What reduces it meanwhile:** the version is pinned rather than floating, so an unreviewed release
cannot arrive on its own; the digest is checked before installation in the image layer; and the
update job opens a pull request rather than publishing by itself.

## Why this agent needs container setup at all

**Recorded 2026-09-12** when Sokar requirement A03 was retired into this repository. Both facts were
measured while the agent was built, and both are the reason `ClaudeContainerSetup` exists rather
than the agent simply being installed and started.

- **It contacts the vendor directly before an interactive session**, ignoring the endpoint it was
  given. So that host has to be reachable even when every model request goes through the broker,
  which is why `claude.yaml` lists `platform.claude.com`, `claude.ai` and `statsig.anthropic.com`
  in `allowed_domains` rather than relying on the provider's host alone.
- **A fresh container has never been logged in**, so the first-run wizard must be answered for it
  or the session stops waiting for input nobody will type. That is what `ClaudeFirstRun` writes,
  and it is why the file is not a secret while the credential file beside it is.
