# CC23 — Sign the RPMs, together with Sokar's

**Status:** soon; blocked by sokar (an issue to be opened).

**What must be true.** A Fedora user installs this adapter with `gpgcheck=1`, and a package whose
signature does not fit is refused.

## Why

`rpm.sign.skip` is `true` everywhere, releases included, and the Fedora `.repo` file uses
`gpgcheck=0`. Sokar's own RPMs are unsigned the same way and say so (`sokar`
`doc/getting-started.md`); the repository metadata is what is signed. Signing this adapter alone
changes nothing for a user, because both share one repository and one `.repo` file.

## Acceptance

- The release job imports the signing key and builds with `-Drpm.sign.skip=false`, in `sokar` and in
  the three agents.
- The `.repo` file uses `gpgcheck=1` with `gpgkey=`, and an acceptance leg installs with it on; an
  unsigned or re-signed package is seen to be refused.
