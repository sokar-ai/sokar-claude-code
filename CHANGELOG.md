# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Headings name this package's version; Claude Code's version is what the package installs and
appears as an entry rather than a heading. One sentence per change - `git log` has the detail.

## [Unreleased]

### Added

- The build refuses an issue number that names no issue, so a citation in prose cannot outlive the issue it points at.
- The build refuses a link to an issue file from anywhere but the index, so a pointer cannot outlive the issue it names.
- The login names Claude Code's authentication page, so an interface can show it beside the button that starts the login.
- The packages provide `sokar-agent`, so the setup script and the daemon list this agent as one a person can choose.
- The Claude Code adapter: definition, credential extraction, headless commands, log formatting.
- `.deb` and `.rpm` packages, published to Artifactory from `main`.
- Claude Code 2.1.236, pinned by version and SHA-256 against Anthropic's per-release manifest.
- A CycloneDX bill of materials in every package, recording the pinned CLI as fetched, not shipped.
- An acceptance suite against the published packages on Ubuntu and Fedora, with a tier that authenticates for real.
- Cucumber scenarios driving a real machine over ssh through Sokar's acceptance kit.
- Weekly automated updates, verifying a new version on both distributions before anything is published.
- `buildtools/check-pin.py`, failing a build whose pinned version, URL and digest disagree.
- `buildtools/check-changelog.py`, failing a code change that does not say what changed.
- This changelog.

### Changed

- The pull request carries the third-party comparison itself, with each component's licence, rather than leaving it in the run log.
- Issues carry their repository's letter: `CC07` rather than `007`, so a number says which set it belongs to.
- The acceptance suite makes its project by following a local repository and names it on every task start; its cleanup asks Sokar to remove the project instead of deleting Sokar's directories.
- Every task the acceptance suite starts names its repository, which Sokar now requires.
- The pinned version, the pom and the download URL are checked by a unit test on the filtered definition the package ships.
- The log formatter drops only the startup line: every other system event, and any event it cannot read, now reaches the operator.
- The README starts a task with `sokar task start`, the name Sokar's lifecycle gives the verb that was `task run`.
- The workflow rents, provisions and deletes its machines with Sokar's Java tooling instead of a copy of a Python script.
- CI says which command it does not know, so tooling older than the caller reads as that rather than as a mistake in the workflow.
- Claude Code pinned to 2.1.274 (was 2.1.236).
- A change that ships nothing observable can say `[no changelog]` in a commit message.
- The installed version is no longer asserted in a unit test, where every bump had to be applied.

### Removed

- The changelog check in CI; requiring an entry returns later, built on logchange.
- `buildtools/ci/` entirely: `sweep.py`, `remote-acceptance.py` and `hetzner.py`, which were a copy of the same helpers in four repositories.

### Fixed

- The packages declare the glibc (2.34) and zlib the native binary links against, and the build fails when the binary needs more.
- The build's index check follows Artifactory's redirect to cloud storage; it had read every package as not indexed.
- A task started without a credential still gets `.claude.json` and `settings.json`; only the credential file waits for a token.
- The update job stops instead of rolling back when upstream offers an older version than is pinned, and compares versions as numbers rather than text.
- The changelog waiver answers for the commit it is written on, rather than for everything pushed with it.
- The changelog check asks whether an entry was added, not whether `CHANGELOG.md` was touched; a rewritten link line used to satisfy it.
- The changelog check reads the waiver after fetching the base commit, not before; in a shallow clone it missed `[no changelog]` and failed the build anyway.
- The changelog check no longer exempts documentation; a typo says `[no changelog]` like any other change that ships nothing observable.
- The acceptance suite refuses a run as root, rather than passing every check but the one that needs the broker.
- The changelog check works in CI's shallow clone, where it could not resolve either commit.

### Security

- Claude Code no longer updates itself inside a task: the pinned version is the one that runs.
- The acceptance suite no longer puts the test credential on a command line; the pattern reaches `grep` on a file descriptor.
- The check that no log holds the credential also searches with line breaks removed, so a value split across a newline is found rather than reported as absent.
- The acceptance run passes the model name to the container as data rather than inside a shell command.
- A credential kind this provider does not store is refused instead of being written as a subscription token.
- The CI no longer installs the unpinned Hetzner Python client; nothing had used it since the Java machine tooling replaced it.
- The update workflow takes its dispatch input through the environment rather than the shell.

[Unreleased]: https://github.com/sokar-ai/sokar-claude-code/commits/main
