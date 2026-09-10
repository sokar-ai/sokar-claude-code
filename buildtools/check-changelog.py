#!/usr/bin/env python3
"""
Fails a change to code that does not say what changed.

A changelog nobody is obliged to write is a changelog that stops being written, and the
first person to notice is whoever is trying to work out what an installed package contains.
The rule this enforces is narrow: if a commit range touches anything that ships or builds,
CHANGELOG.md has to be in that range too.

    check-changelog.py <base> <head>

Documentation and editor settings are exempt, because a typo fix is not a notable change and
requiring an entry for one teaches people to write entries that say nothing.

Exit codes:

    0   the changelog was updated, or nothing needed it
    1   code changed and the changelog did not
    2   the range could not be read

A NOTE ON WHAT THIS CANNOT SEE. It compares two commits. On the first push of a new branch
there is no base to compare against, and GitHub reports the previous commit as all zeros -
so the check says so and passes rather than failing every new branch. That is a real hole,
and it is stated here rather than left for someone to discover: the check is a reminder for
the ordinary case, not a wall.
"""
from __future__ import annotations

import subprocess
import sys
from fnmatch import fnmatch

CHANGELOG = "CHANGELOG.md"

# Changing one of these needs no entry. Everything else does - including the build files and
# the workflows, which decide what an operator receives just as much as the source does.
EXEMPT = ("*.md", ".gitignore", ".idea/*", "LICENSE")

EMPTY = "0" * 40


def changed(base: str, head: str) -> list[str]:
    """
    Lists the files that differ between two commits.

    :param base: What to compare from.
    :param head: What to compare to.
    :return: Repository-relative paths.
    """
    try:
        out = subprocess.run(["git", "diff", "--name-only", f"{base}..{head}"],
                             capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as failure:
        print(f"could not read {base}..{head}: {failure.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return [line for line in out.stdout.splitlines() if line]


def main() -> int:
    base, head = sys.argv[1], sys.argv[2]

    if not base or base.startswith(EMPTY[:8]):
        print(f"::warning::no commit to compare against ({base!r}), so the changelog was not "
              f"checked. This is not the same as 'it was updated'.")
        return 0

    files = changed(base, head)
    if not files:
        print("nothing changed in this range")
        return 0

    if CHANGELOG in files:
        print(f"{CHANGELOG} is in this change")
        return 0

    needing = [f for f in files if not any(fnmatch(f, pattern) for pattern in EXEMPT)]
    if not needing:
        print(f"only documentation and settings changed, so {CHANGELOG} is not required")
        return 0

    print(f"::error::{CHANGELOG} was not updated, but this change touches what ships:")
    for f in needing:
        print(f"  {f}")
    print()
    print(f"Add what changed under '## [Unreleased]' in {CHANGELOG}. A version bump applied by")
    print("buildtools/update.py writes its own entry and needs nothing by hand.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
