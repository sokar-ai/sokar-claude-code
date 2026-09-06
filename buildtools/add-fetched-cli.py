#!/usr/bin/env python3
"""
Adds the CLI this agent installs to its bill of materials.

The package does not contain that CLI - the image build fetches it from a pinned URL and
checks it against a digest - so nothing that reads the Maven dependency graph can know about
it. A bill that omits the largest thing an image installs is worse than no bill, so it is
recorded here and marked as fetched rather than shipped.

Read from the FILTERED definition in target/classes rather than from the POM: that is the file
the agent binary answers `describe` with, so the version and digest recorded are the ones an
image build will actually use.

    add-fetched-cli.py <bom.json> <agent.yaml>
"""
import json
import re
import sys


def main() -> int:
    bom_path, yaml_path = sys.argv[1], sys.argv[2]

    text = open(yaml_path, encoding="utf-8").read()
    version = re.search(r'^\s*version:\s*"?([^"\n]+)"?', text, re.M)
    url = re.search(r'^\s*-?\s*url:\s*(\S+)', text, re.M)
    digest = re.search(r'^\s*sha256:\s*"?([0-9a-f]{64})"?', text, re.M)
    if not (version and url):
        print("add-fetched-cli: no pinned artifact in " + yaml_path + ", nothing to add")
        return 0

    with open(bom_path, encoding="utf-8") as handle:
        bom = json.load(handle)

    component = {
        "type": "application",
        "name": "claude-code",
        "version": version.group(1),
        "purl": f"pkg:generic/claude-code@{version.group(1)}?download_url={url.group(1)}",
        "externalReferences": [{"type": "distribution", "url": url.group(1)}],
        # Not in this package. An image build fetches it, so a reader of the bill knows to look
        # for it there rather than in the payload.
        "properties": [{"name": "sokar:delivery", "value": "fetched-at-image-build"}],
    }
    if digest:
        component["hashes"] = [{"alg": "SHA-256", "content": digest.group(1)}]

    bom.setdefault("components", []).append(component)
    with open(bom_path, "w", encoding="utf-8") as handle:
        json.dump(bom, handle, indent=2)
    print(f"add-fetched-cli: recorded claude-code {version.group(1)} as fetched, not shipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
