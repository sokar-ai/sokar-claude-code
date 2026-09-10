#!/usr/bin/env python3
"""
Moves this module to a new Claude Code version, doing exactly what a person would.

    update.py <version> [--dry-run]

Two things are written by hand today and both are written here:

    pom.xml                             <agent.cli.version>
    src/main/resources/agent/claude.yaml    the SHA-256 of the linux-x64 binary

Everything else that names the version - the definition's install section, the download URL,
the package description in both the deb and the rpm - is FILTERED from that property, so it
cannot be left behind. That is deliberate and worth keeping: the fewer places a bot writes,
the fewer places it can half-write.

The digest is never taken from the caller. It is read from the per-version manifest Anthropic
publishes at

    https://downloads.claude.ai/claude-code-releases/<version>/manifest.json

so a version that does not exist, or one published without a linux-x64 build, stops here
instead of becoming a package whose image build fails at 'sha256sum -c'.

THE MODULE'S OWN VERSION IS NOT BUMPED WHILE IT IS A SNAPSHOT. 'agent.snapshot.run' - the CI
run number - already makes every build a strictly newer package than the last, which is what
apt and dnf sort on, and 1.0.1-SNAPSHOT would invent a successor to a 1.0.0 that was never
released. Once a release exists, a CLI move is a patch bump of the module, and this does that.

Exit codes:

    0   the working tree now pins the requested version
    1   the request cannot be carried out - no such release, no linux-x64 build, nothing to write
    2   upstream could not be read, which is not the same as "no such version"
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

# One entry: a second platform would be a package change, not a version change.
PLATFORM = "linux-x64"

VERSION = re.compile(r"^\d+\.\d+\.\d+$")

ROOT = Path(__file__).resolve().parents[1]
POM = ROOT / "pom.xml"
DEFINITION = ROOT / "src" / "main" / "resources" / "agent" / "claude.yaml"


def manifest(version: str) -> dict:
    """
    Reads the per-version manifest, which is what makes the pin verifiable rather than trusted.

    :param version: The release to look up.
    :return: The parsed manifest.
    """
    url = f"{RELEASES}/{version}/manifest.json"
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as failure:
        if failure.code == 404:
            print(f"there is no release {version} - {url} answers 404", file=sys.stderr)
            sys.exit(1)
        unreadable(f"{url}: HTTP {failure.code}")
    except Exception as failure:  # noqa: BLE001 - any failure here means "do not know"
        unreadable(f"{url}: {failure}")
    return {}  # unreachable; unreadable() exits


def unreadable(reason: str):
    """
    Stops with the code that means "could not ask", distinct from "asked and the answer is no".

    A caller that treats them alike will eventually read a proxy outage as a withdrawn release.
    """
    print(f"could not read the manifest - {reason}", file=sys.stderr)
    print("This is not the same as 'there is no such version'.", file=sys.stderr)
    sys.exit(2)


def replace_once(text: str, pattern: re.Pattern, replacement, what: str) -> str:
    """
    Substitutes exactly one occurrence, refusing zero and refusing several.

    A bot that writes nothing and reports success is the failure this whole pipeline exists to
    avoid, and a bot that writes a second occurrence it did not know about is worse. Both are
    silent with a plain re.sub.

    :param text: What to rewrite.
    :param pattern: What to find.
    :param replacement: Passed to re.sub.
    :param what: Named in the error, so a failure says which file gave up.
    :return: The rewritten text.
    """
    rewritten, count = pattern.subn(replacement, text)
    if count != 1:
        print(f"expected exactly one {what}, found {count} - refusing to guess", file=sys.stderr)
        sys.exit(1)
    return rewritten


def main() -> int:
    parser = argparse.ArgumentParser(description="Pins a new Claude Code version.")
    parser.add_argument("version", help="the release to pin, e.g. 2.1.267")
    parser.add_argument("--dry-run", action="store_true",
                        help="say what would change and write nothing")
    args = parser.parse_args()

    if not VERSION.match(args.version):
        print(f"{args.version!r} is not a version", file=sys.stderr)
        return 1

    platforms = manifest(args.version).get("platforms") or {}
    build = platforms.get(PLATFORM)
    if not build or not build.get("checksum"):
        print(f"{args.version} publishes no {PLATFORM} checksum - "
              f"it has {sorted(platforms) or 'no platforms at all'}", file=sys.stderr)
        return 1
    digest = build["checksum"]

    pom = POM.read_text(encoding="utf-8")
    was = re.search(r"<agent\.cli\.version>([^<]+)</agent\.cli\.version>", pom)
    if not was:
        print(f"{POM} declares no agent.cli.version", file=sys.stderr)
        return 1
    if was.group(1).strip() == args.version:
        print(f"already pinned to {args.version} - nothing to do")
        return 0

    pom = replace_once(pom, re.compile(r"<agent\.cli\.version>[^<]+</agent\.cli\.version>"),
                       f"<agent.cli.version>{args.version}</agent.cli.version>",
                       "agent.cli.version in pom.xml")

    definition = DEFINITION.read_text(encoding="utf-8")
    definition = replace_once(definition, re.compile(r'(\bsha256:\s*")[0-9a-f]{64}(")'),
                              lambda m: f"{m.group(1)}{digest}{m.group(2)}",
                              "pinned sha256 in claude.yaml")

    module = re.search(r"<artifactId>sokar-agent-claude</artifactId>\s*<version>([^<]+)</version>",
                       pom)
    bumped = None
    if module and not module.group(1).endswith("-SNAPSHOT"):
        major, minor, patch = module.group(1).split(".")
        bumped = f"{major}.{minor}.{int(patch) + 1}"
        pom = replace_once(
            pom,
            re.compile(r"(<artifactId>sokar-agent-claude</artifactId>\s*<version>)"
                       r"[^<]+(</version>)"),
            lambda m: f"{m.group(1)}{bumped}{m.group(2)}", "the module's own version")

    print(f"  claude code   {was.group(1).strip()} -> {args.version}")
    print(f"  sha256        {digest}  ({PLATFORM}, from the published manifest)")
    if bumped:
        print(f"  this module   {module.group(1)} -> {bumped}")
    elif module:
        print(f"  this module   {module.group(1)}, unchanged - the CI run number already orders "
              f"snapshot packages")

    if args.dry_run:
        print("\n--dry-run: nothing written")
        return 0

    POM.write_text(pom, encoding="utf-8")
    DEFINITION.write_text(definition, encoding="utf-8")
    print(f"\nwritten. Review the diff, then: Pin Claude Code {args.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
