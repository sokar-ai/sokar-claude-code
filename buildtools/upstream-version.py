#!/usr/bin/env python3
"""
Says whether Claude Code has moved on from the version this module pins.

The first step of the update pipeline, and the one that differs most between agents: what
"the current version" even is depends on how the vendor publishes. Anthropic serves two
plain-text pointers beside the per-version manifests, so this reads one of them; another
agent reads a registry. What every agent's copy of this script shares is the OUTPUT, so the
job that calls it does not have to know which:

    pinned=2.1.236       what this module installs today
    upstream=2.1.267     what the chosen channel points at
    update=yes           'yes' when newer, 'no' when the same, 'rollback' when older
    source=channel stable  which pointer 'upstream' was read from
    major=same           'moved' when the major version changed, which nothing may decide alone

The same lines are appended to $GITHUB_OUTPUT when it is set, so a workflow reads them as
step outputs without parsing anything.

Exit codes:

    0   the question was answered, whatever the answer is
    2   it could not be answered

'update=yes' is deliberately NOT a non-zero exit. A scheduled job that goes red every time
there is something to do teaches whoever watches it to ignore red, and then a real failure
looks the same as an ordinary Tuesday.

CHANNELS, measured 2026-09-10:

    .../claude-code-releases/stable  ->  2.1.236
    .../claude-code-releases/latest  ->  2.1.267

'stable' is what this follows, and it is what the module pins today. Whether a release should
have to reach a certain age before it is picked up is a question upstream already answers, so
there is no heuristic to invent here; --channel latest opts out of that judgement and into none.

THE GAP BETWEEN THE TWO IS AN OBSERVATION, NOT A CONTRACT. On the date above it was 31 patch
releases and three weeks; nothing published says it will stay near that, and the two converging,
or 'stable' moving twice in a day, would both be normal. Nothing here may assume a minimum age.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RELEASES = "https://downloads.claude.ai/claude-code-releases"

# What a version has to look like before anything is done with it. A pointer file that starts
# serving an error page, an HTML redirect or an empty body would otherwise travel all the way
# into a pom property and be discovered as a build failure two steps later.
VERSION = re.compile(r"^\d+\.\d+\.\d+$")

POM = Path(__file__).resolve().parents[1] / "pom.xml"


def pinned() -> str:
    """
    Reads the version this module installs, from the one place it is written by hand.

    Everything else - the definition's install section, the download URL, the package
    description - is filtered from this property, so this is the pin and the rest cannot
    disagree with it.
    """
    text = POM.read_text(encoding="utf-8")
    found = re.search(r"<agent\.cli\.version>([^<]+)</agent\.cli\.version>", text)
    if not found:
        unanswerable(f"{POM} declares no agent.cli.version")
    version = found.group(1).strip()
    if not VERSION.match(version):
        unanswerable(f"{POM} pins {version!r}, which is not a version")
    return version


def upstream(channel: str) -> str:
    """
    Reads the version the channel points at.

    :param channel: 'stable' or 'latest'; anything else is passed through, because the set is
        the vendor's to change and guessing it here would be one more thing to keep in step.
    """
    url = f"{RELEASES}/{channel}"
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            body = response.read().decode("utf-8").strip()
    except urllib.error.HTTPError as failure:
        unanswerable(f"{url}: HTTP {failure.code}")
    except Exception as failure:  # noqa: BLE001 - anything at all here means "do not know"
        unanswerable(f"{url}: {failure}")
    if not VERSION.match(body):
        unanswerable(f"{url} did not answer with a version: {body[:80]!r}")
    return body


def unanswerable(reason: str):
    """
    Stops with the code that means "could not tell", which is not the code for "up to date".

    The distinction is the whole point of having one. An update job that reads a failed fetch
    as "nothing new" is quietly switched off, and looks exactly like one that is working.
    """
    print(f"could not tell whether there is a new version - {reason}", file=sys.stderr)
    sys.exit(2)


def order(version: str) -> tuple[int, ...]:
    """
    Returns a version as something that sorts the way versions do.

    As text, 2.1.9 sorts after 2.1.10, and a gate that calls a legitimate update a rollback gets
    switched off. VERSION has already refused anything but three numbers, so this is the whole
    comparison rather than a parser for one.

    :param version: A version that matched VERSION.
    :return: Its numbers, in order.
    """
    return tuple(int(part) for part in version.split("."))


def verdict(have: str, there: str, named: bool) -> str:
    """
    Decides what the job does about the two versions.

    Older than the pin is a rollback, which automation may not choose: a withdrawn release and
    two pointers that disagree look the same from here. Only a version a person named may take
    the pin backwards.

    :param have: The pinned version.
    :param there: The version upstream offers.
    :param named: Whether a person named that version rather than a pointer.
    :return: 'yes', 'no' or 'rollback'.
    """
    if order(there) > order(have):
        return "yes"
    if order(there) == order(have):
        return "no"
    return "yes" if named else "rollback"


def main() -> int:
    parser = argparse.ArgumentParser(description="Compares the pinned Claude Code version "
                                                 "against the one upstream publishes.")
    parser.add_argument("--channel", default="stable",
                        help="the pointer to follow; 'stable' by default, which is upstream's "
                             "own judgement about what is ready")
    # Overriding upstream, not the pin: 'major' must compare against what this module installs.
    parser.add_argument("--upstream", default=None, metavar="VERSION",
                        help="answer as if the channel pointed at this version, and ask nothing")
    args = parser.parse_args()

    have = pinned()
    there = args.upstream or upstream(args.channel)
    if args.upstream and not VERSION.match(there):
        print(f"{there!r} is not a version", file=sys.stderr)
        return 1

    answer = {
        "pinned": have,
        "upstream": there,
        "source": "a version named by hand" if args.upstream else f"channel {args.channel}",
        "update": verdict(have, there, bool(args.upstream)),
        # Answered here rather than by the caller, so every agent's copy answers it the same way.
        "major": "moved" if there.split(".")[0] != have.split(".")[0] else "same",
    }

    for key, value in answer.items():
        print(f"{key}={value}")

    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            for key, value in answer.items():
                handle.write(f"{key}={value}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
