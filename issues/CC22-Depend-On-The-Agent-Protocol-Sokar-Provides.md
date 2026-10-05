# CC22 — Depend on the agent protocol Sokar's package provides

**Status:** later; blocked by sokar (an issue to be opened).

**What must be true.** Installing this adapter beside a Sokar that speaks another agent protocol is
refused by the package manager, not at the first task.

## Why

Both packages require only `sokar` (`src/deb/control/control`, `pom.xml` `<require>`), with no
version, while the adapter is built against one agent contract. It is not a live defect: Sokar checks
an adapter's `protocolVersion` before using it and refuses a mismatch with a message
(`agents/api/.../InstalledAgent.java`), but that refusal comes at the first task.

## Acceptance

- Sokar's packages declare `Provides: sokar-agent-protocol-<N>` (deb and rpm).
- This adapter's packages depend on that instead of on `sokar` alone, and a test holds the declared
  number to the API's `AgentProtocol.VERSION`; it is seen to fail with the numbers apart.
- The same in `sokar-pi` and `sokar-omp`.
