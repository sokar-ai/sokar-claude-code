# Decisions

Settled reasoning that outlives the change that produced it. A decision is written here when
somebody would otherwise ask "why is it like this?" and find only code.

Accepted risks live here too. An accepted risk is not a forgotten one: it says what the exposure
is, why it is not being removed, and what would change the answer.

Newest first, and in the order they stand below. The date is when the decision was taken,
not when its row was written - the older ones were found with `git log -S` on the sentence
rather than guessed.

| Date | What was decided |
|---|---|
| 2026-09-13 | [The changelog check is removed, not replaced](#the-changelog-check-is-removed-not-replaced) - requiring an entry returns with Sokar B55, on logchange |
| 2026-09-13 | [The API-key dialog is answered, because the key is the task's own](#the-api-key-dialog-is-answered-because-the-key-is-the-tasks-own) - reverses the refusal of 2026-09-09 |
| 2026-09-12 | [Accepted risk: the release binary and its digest share one trust root](#accepted-risk-the-release-binary-and-its-digest-share-one-trust-root) - nothing independent to verify the download against, and why that stays |
| 2026-09-04 | [Why this agent needs container setup at all](#why-this-agent-needs-container-setup-at-all) - it calls the vendor before a session, and a fresh container has never logged in |
| 2026-09-03 | [What was actually proven about brokering this agent](#what-was-actually-proven-about-brokering-this-agent) - which transport, which credential kind, against what |

## The changelog check is removed, not replaced

**Decided 2026-09-13 by the operator**, across all Sokar repositories.

`buildtools/check-changelog.py` failed a push whose code change did not touch `CHANGELOG.md`. It is
deleted, and nothing replaces it for now. Sokar is moving to logchange - one YAML file per change,
and a generated `CHANGELOG.md` - and a check for a hand-kept file would have to be rebuilt the moment
that reaches this repository. Requiring an entry returns as Sokar B55, proposed to logchange upstream
first, which keeps the three lessons the script carried: a waiver answers for its own commit only,
documentation is not exempt, and a range that cannot be compared fails.

**Until then** the changelog is still written by hand in the same commit; only the enforcement is gone.

**What would change it:** B55 landing, or logchange being adopted here.

## The API-key dialog is answered, because the key is the task's own

**Decided 2026-09-13 by the operator, reversing 2026-09-09.**

Started with a token in its environment, Claude Code asks whether to use *"a custom API key"* and
recommends **No**. The refusal of 2026-09-09 held that answering it would decide billing on
somebody's behalf. What was measured since changes the premise: the key shown is the **phantom
token Sokar minted for this task**, not a payment credential. The billing decision was made earlier
and elsewhere - when the operator put the real credential into the vault and chose a provider.

**The recommended answer is the harmful one.** Taking *No* refuses the only credential the task
has, in a dialog that describes it as suspicious. Unattended there is nobody to answer at all.

**How it is answered, measured 2026-09-10 on Claude Code 2.1.267:** the last 20 characters of the
token under `customApiKeyResponses.approved` in `.claude.json` remove the dialog completely.

**What would change the answer:** the environment carrying a real payment credential instead of a
task-scoped token. Then this would be a billing decision again, and it would be asked.

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

## What was actually proven about brokering this agent

**Recorded 2026-09-12** from Sokar requirement A03 before it was retired, because "verified" without
the shape of the verification is a claim rather than a record.

It honors **both** a base URL and a unix socket, with **either** credential kind - an API key or a
subscription token - **including a token minted for the task** rather than the real credential. That
is why `claude.yaml` sets `ANTHROPIC_UNIX_SOCKET` and `ANTHROPIC_BASE_URL` together: the socket
selects the transport, and without the base URL the CLI falls back to its compiled-in endpoint. That
fallback was measured - it resolved `api.anthropic.com` 184 times in one run and never touched the
socket.
