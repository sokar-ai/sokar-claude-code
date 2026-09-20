# CC04 — Automated agent updates: what is still undecided

**Priority:** 2
**Opened:** 2026-09-12
**Source:** handed over from Sokar requirement **A02**, 2026-09-12. The requirement covered all
three agent repositories; this is this repository's share of it.
**Depends on:** the same issue in `sokar-pi` and `sokar-omp` - any rule agreed here should be the
same rule there, or the divergence should be deliberate.

## What is already built here

Detect, apply, verify, publish all exist: `buildtools/upstream-version.py` reads Anthropic's
`stable` pointer, `buildtools/update.py` moves the pin, `buildtools/check-pin.py` refuses a
disagreement between the places that name a version, `buildtools/compare-bills.py` stops a release
that changes what third-party code ships, and the weekly job runs them. A rollback is never
automatic: an older upstream version stops the run red rather than moving the pin backwards.

So this issue is not "build the pipeline". It is the set of questions the pipeline still answers by
convention rather than by a stated rule.

## What is still open

- **Can the verifying tier's credential live in CI?** Without it the automation checks less than a
  person does by hand, which is a worse gate wearing the appearance of a better one. Today the key
  is in the workflow's secrets and the tier runs; what is undecided is whether that is the intended
  arrangement or a temporary one.
- **What version does the agent package take when only the tool it installs moved?** The two were
  separated deliberately. A bot needs a stated rule rather than a guess.
- **Is `stable` the right thing to follow?** Upstream already applies an ageing rule to that
  pointer, which is why it is followed rather than `latest` - but nothing here states how old a
  release must be if that ever stops being true.
- **How do the CI snapshots get refreshed when GraalVM or the base image moves?** The same question
  one layer down: the machines pin GraalVM by digest and pre-pull base images, so following an
  upstream release there means rebuilding an image rather than editing a version.

## What would close it

Each question answered in `doc/decisions.md` with its reasoning, and where the answer is a rule the
pipeline must keep, a check that fails when it is broken. An answer that lives only in a person's
head is what this issue exists to remove.
