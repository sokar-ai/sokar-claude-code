# CC17 — Record the fetched CLI in the bill of materials

**Priority:** 2
**Opened:** 2026-09-27
**Source:** measured while carrying the third-party comparison into the pull request, 2026-09-27

## What

The published bill of materials names **5 components** — this module's own Java dependencies. The
thing this package exists to install, the pinned Claude Code binary, is not one of them. Measured on
2026-09-27 against
`https://fuinorg.jfrog.io/artifactory/sokar-dist-deb/pool/main/s/sokar-agent-claude/sokar-agent-claude.cdx.json`:
5 components, against `sokar-pi`'s 140, because that repository builds an npm tree from a lockfile
and this one fetches one file.

So `buildtools/compare-bills.py` compares five Java libraries that an upstream release cannot
change, and the licence gate in `update.yml` is one the update can hardly ever trip. **This
repository's step does not say so and `sokar-omp`'s does** - *"A no-op today: this bill does not
record the fetched binary, so nothing moves."* The same is true here and is written down nowhere,
which is why it reads as a working gate.

**What it costs today:** a Claude Code release that changes its own licence, or that bundles something
new, reaches a package with nothing asking. The gate that would catch it is the one place a person
was meant to look, and for this repository it looks at the wrong five things.

**Why the shape is already decided:** `update.yml` passes `--expect-moved claude-code`, which exists so that
the pinned CLI moving version does not stop every update. **That argument is only needed once the
binary is in the bill**, so the design anticipated this and the recording was never built.

## What would close it

- The bill names the pinned CLI as a component: its version, the URL it came from, the SHA-256 the
  definition pins, and the licence upstream declares.
- `compare-bills.py` reports it as `moved` on a version bump rather than as one added and one
  removed, which `--expect-moved claude-code` already does once the component exists.
- A release whose licence changed stops the update, proven by running the comparison against a bill
  with the licence altered by hand.
- `sokar-omp` has the same gap as `OM14`; whatever is written here is written there, because
  both fetch a single binary rather than building a tree.

## Open question

Where the licence comes from. The definition pins a URL and a digest, not a licence, and reading it
from the release page would be a network call in a build that has one already for the digest.
Whether the manifest.json Anthropic publishes beside each release is the source, or the repository's declared licence,
or a value in the agent definition, is not decided here.
