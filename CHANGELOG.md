# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Two different versions appear here and they move independently. **This package's version**
is what the headings below name. **Claude Code's version** is what the package installs,
recorded as an entry rather than as a heading, because a new CLI is a change to what this
package delivers and not a change to this package's own interface.

Nothing has been released yet, so everything so far is unreleased.

## [Unreleased]

### Added

- The Claude Code adapter: the agent definition, OAuth and API-key extraction from the
  credentials file the CLI writes at login, headless command building, `stream-json` log
  formatting, and the container setup that fetches and verifies the CLI.
- `.deb` and `.rpm` packages installing into `/usr/libexec/sokar/agents`, where Sokar scans
  for agents, published to Artifactory from `main`.
- Claude Code 2.1.236, pinned by version and SHA-256 against the manifest Anthropic
  publishes per release, so an image build verifies what it fetches.
- A CycloneDX bill of materials in every package, at `/usr/share/sokar/sbom/`, recording the
  pinned CLI the package does *not* contain as fetched rather than shipped.
- An acceptance suite run against the published packages on rented Ubuntu and Fedora
  machines, including a tier that authenticates against a real provider and checks the
  credential reaches no container and no log.
- Cucumber scenarios driving a real machine over ssh through Sokar's published acceptance
  kit, run from CI on every push to `main`.
- Weekly automated updates (`.github/workflows/update.yml`): follow Anthropic's `stable`
  channel, apply the new pin, rebuild, and prove the result on both distributions against
  the packages built in that run before anything is published. It opens a pull request and
  never merges by itself.
- `buildtools/update.py`, which applies a new Claude Code version: the pinned version, the
  SHA-256 read from that release's manifest, and this file.
- `buildtools/check-pin.py`, run on every push: the pinned version, the download URL and
  the digest must agree with each other and with what Anthropic publishes.
- `buildtools/check-changelog.py`, which fails a change to code that does not say what
  changed here.
- `--candidate` on the acceptance runner, installing packages built in the run instead of
  published ones, so an update is proved before it is published rather than after.
- `--expect-moved` on `compare-bills.py`, so the component an update is deliberately moving
  does not read as one component added and another removed.

### Changed

- Claude Code pinned to 2.1.267 (was 2.1.236).
- The version a package installs is no longer written in a unit test. It was, and that made
  the test a place every version bump had to be applied, so a correct update went red and
  the way to get green was to edit an assertion.

### Security

- The dispatch input of the update workflow is passed through the environment rather than
  interpolated into a shell script, where it would have reached the shell before being
  checked.

[Unreleased]: https://github.com/fuinorg/sokar-claude-code/commits/main
