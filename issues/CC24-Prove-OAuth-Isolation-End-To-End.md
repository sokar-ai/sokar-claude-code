# CC24 — Prove OAuth isolation end to end

**Status:** later.

**What must be true.** A task started with a Claude subscription holds only its own short-lived token:
the refresh token never reaches it, and only the host renews.

## Why

The acceptance scenarios run with an OpenRouter API key only. OAuth is covered by unit tests here
(`ClaudeCredentialExtractorTest`, `ClaudeContainerSetupTest`) and by Sokar's own tests and its
stub-agent `agent-login.feature`; no scenario signs in with a subscription and looks inside a Claude
Code task. A live subscription in CI would spend a person's login: every renewal rotates the refresh
token.

## Acceptance

- A scenario shows the task holds only its own token, and the refresh token is in neither its
  environment nor its files nor the logs.
- A renewal from inside the task is seen to be refused, and the host renews.

## To be checked

- Whether the scenario runs against a fake token endpoint or a dedicated CI subscription.
