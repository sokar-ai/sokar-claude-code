# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Headings name this package's version; Claude Code's version is what the package installs and
appears as an entry rather than a heading. One sentence per change - `git log` has the detail.

## [Unreleased]

### Changed

- The workflow deletes its rented machines with Sokar's Java tooling instead of a copy of a Python script.

### Removed

- `buildtools/ci/sweep.py`, and the sweeping half of `buildtools/ci/hetzner.py`.

### Added

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

- Claude Code pinned to 2.1.267 (was 2.1.236).
- The installed version is no longer asserted in a unit test, where every bump had to be applied.

### Security

- The update workflow takes its dispatch input through the environment rather than the shell.

### Fixed

- The changelog check works in CI's shallow clone, where it could not resolve either commit.

[Unreleased]: https://github.com/fuinorg/sokar-claude-code/commits/main
