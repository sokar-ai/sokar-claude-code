#!/usr/bin/env python3
"""
Checks that everything naming the pinned Claude Code version says the same thing.

Nothing enforced this before. A bot that writes one place and not another would ship a package
whose definition advertises a version its own payload does not install, and no test would
notice until an image build failed on somebody else's machine.

Read from the FILTERED definition in target/classes, not from src: that is the file the agent
binary answers 'describe' with, so it is what an image build will actually use. Reading the
source template would check the template and prove nothing about the build.

    check-pin.py [--definition target/classes/agent/claude.yaml] [--offline]

Four questions, in the order they get cheaper to be wrong about:

    1  the version is a version, not an unsubstituted ${...} - filtering happened at all
    2  it is the version pom.xml pins
    3  the download URL names that same version
    4  the digest is the one Anthropic publishes for it   (--offline skips this one)

The fourth is the only one that can drift in this repository today, and it is the one that
needs the network: the version travels into the definition, the URL and both package
descriptions by resource filtering, so those cannot disagree. The digest is typed in.

Exit codes:

    0   they agree
    1   they do not
    2   the question could not be answered - the manifest was unreachable, which is not agreement
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RELEASES = "https://downloads.claude.ai/claude-code-releases"
PLATFORM = "linux-x64"

ROOT = Path(__file__).resolve().parents[1]
POM = ROOT / "pom.xml"
FILTERED = ROOT / "target" / "classes" / "agent" / "claude.yaml"

FAILURES = 0


def ok(message: str) -> None:
    print(f"  \033[32mOK\033[0m    {message}")


def bad(message: str) -> None:
    global FAILURES
    print(f"  \033[31mFAIL\033[0m  {message}")
    FAILURES += 1


def unanswerable(reason: str):
    """Stops with the code that means "could not check": a proxy outage is not agreement."""
    print(f"  \033[33mUNKNOWN\033[0m  {reason}")
    print("Could not check the digest. This is not the same as 'it agrees'.", file=sys.stderr)
    sys.exit(2)


def published_digest(version: str) -> str:
    """
    Reads the SHA-256 Anthropic publishes for the linux-x64 build of one release.

    :param version: The release to look up.
    :return: The 64-character digest.
    """
    url = f"{RELEASES}/{version}/manifest.json"
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            platforms = json.load(response).get("platforms") or {}
    except urllib.error.HTTPError as failure:
        # A 404 is an answer, and a bad one: the definition pins a release that is not there.
        if failure.code == 404:
            bad(f"there is no release {version} - {url} answers 404")
            sys.exit(1)
        unanswerable(f"{url}: HTTP {failure.code}")
    except Exception as failure:  # noqa: BLE001
        unanswerable(f"{url}: {failure}")
    build = platforms.get(PLATFORM) or {}
    if not build.get("checksum"):
        bad(f"{version} publishes no {PLATFORM} checksum")
        sys.exit(1)
    return build["checksum"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Checks that the pinned version agrees "
                                                 "everywhere it appears.")
    parser.add_argument("--definition", default=str(FILTERED),
                        help="the FILTERED definition, as built into target/classes")
    parser.add_argument("--offline", action="store_true",
                        help="skip the digest check, which is the only one needing the network")
    args = parser.parse_args()

    definition = Path(args.definition)
    if not definition.is_file():
        print(f"{definition} does not exist - build first, this reads what the build produced",
              file=sys.stderr)
        return 2

    text = definition.read_text(encoding="utf-8")
    version = re.search(r'^\s*version:\s*"?([^"\n]+)"?\s*$', text, re.M)
    url = re.search(r"^\s*-?\s*url:\s*(\S+)\s*$", text, re.M)
    digest = re.search(r'^\s*sha256:\s*"?([0-9a-f]{64})"?\s*$', text, re.M)

    if not (version and url and digest):
        bad(f"{definition} has no complete pinned artifact - "
            f"version={bool(version)} url={bool(url)} sha256={bool(digest)}")
        return 1
    version, url, digest = version.group(1).strip(), url.group(1), digest.group(1)

    print(f"== the pin, as {definition} carries it ==")

    if "${" in version or "${" in url:
        bad(f"resource filtering did not run - the definition still reads {version!r}")
        return 1
    ok(f"the definition installs Claude Code {version}")

    pinned = re.search(r"<agent\.cli\.version>([^<]+)</agent\.cli\.version>",
                       POM.read_text(encoding="utf-8"))
    if not pinned:
        bad("pom.xml declares no agent.cli.version")
    elif pinned.group(1).strip() != version:
        bad(f"pom.xml pins {pinned.group(1).strip()}, the definition installs {version}")
    else:
        ok("pom.xml pins the same version")

    if f"/{version}/" not in url:
        bad(f"the download URL does not name {version}: {url}")
    else:
        ok("the download URL names it")

    if args.offline:
        print("  \033[33mSKIP\033[0m  the digest, --offline")
    else:
        expected = published_digest(version)
        if expected != digest:
            bad(f"the digest is not the one published for {version}\n"
                f"          definition {digest}\n"
                f"          published  {expected}")
        else:
            ok(f"the digest is the published {PLATFORM} one")

    print()
    if FAILURES:
        print(f"STOP: {FAILURES} of the pinned facts disagree. An image build would install "
              f"something other than what this package advertises.")
        return 1
    print("The pin agrees everywhere it is written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
