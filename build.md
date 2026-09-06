# Building

Nothing here needs a checkout of [Sokar](https://github.com/fuinorg/sokar). This
repository compiles against the **published agent contract** - `sokar-agent-api`
and `sokar-wire` - resolved from Maven, and that is the property worth keeping: if
a build here ever needs the Sokar sources, the split has been undone without
anyone deciding to undo it.

```
./mvnw -s settings.xml verify                     # unit tests
./mvnw -s settings.xml -Pnative,dist verify       # + the binary, the .deb and the .rpm
```

`-s settings.xml` is not optional while the contract is a snapshot: it declares the
repository the snapshot comes from. The native build needs GraalVM as `JAVA_HOME`.

What the second command leaves in `target/`:

```
sokar-agent-claude                              the adapter, run by Sokar on the host
sokar-agent-claude_1.0.0~SNAPSHOT_amd64.deb
sokar-agent-claude-1.0.0~SNAPSHOT-1.x86_64.rpm
```

**The package version is this agent's own**, not Sokar's. An agent released against
an unchanged CLI is still an upgrade, and a Sokar release does not move it. `~`
rather than `-` before `SNAPSHOT` because dpkg and rpm sort `~` below everything;
left as `-SNAPSHOT` it would sort *above* the release and apt would refuse the
upgrade.

The Claude Code version the image installs is carried in the package description
instead, so `dpkg -s sokar-agent-claude` and `rpm -qi` still answer it.

## Bumping the CLI version

`src/main/resources/agent/claude.yaml` pins one version and one digest:

```yaml
install:
  version: "${agent.cli.version}"
  artifacts:
    - url: https://downloads.claude.ai/claude-code-releases/${agent.cli.version}/linux-x64/claude
      sha256: "6c8818fa…"
```

Anthropic publishes a per-version `manifest.json` carrying a SHA-256 per
platform, at
`https://downloads.claude.ai/claude-code-releases/<version>/manifest.json`, so
this is verifiable rather than trusted. Bumping is a two-line change: the `agent.cli.version`
property in `pom.xml` and the digest here. Until it is bumped, every image build
installs the same bytes.

`sokar agents --supply-chain` reports what is pinned, so "which version ran" is
answerable from the installed adapter rather than from a build log.

## What this repository cannot check

The acceptance suite needs podman, nftables and a `sokar` binary, so it lives in the
Sokar repository. What is provable here is that the adapter compiles against the
contract, that its unit tests pass, and that it packages. Whether a real CLI honours
the socket and stays inside its declared domains is checked by
`buildtools/e2e-tier1.sh` over there.
