# Issues

What is open in this repository, ordered by what to do next rather than by number. The number is
identity, not sequence.

| # | Status | Blocked by | What it covers | Open questions |
|---|---|---|---|---|
| [CC08](CC08-Approve-The-Task-Token-At-First-Run.md) | open | — | The API-key dialog shows the task's own token and recommends refusing it; decided to answer it in the first-run file. | 0 |
| [CC06](CC06-Which-Setting-Silences-The-Bypass-Warning.md) | open | — | Which of the two settings keys silences the bypass-mode warning. | 1 |
| [CC07](CC07-Drop-The-Skip-Permissions-Flag.md) | blocked | CC06 | Dropping the flag that raises the bypass-mode warning. | 0 |
| [CC12](CC12-Replace-The-Build-Time-Python-Tools.md) | blocked | Sokar B53 | The Python tool every package build runs, replaced by the tool Sokar publishes. | 0 |
| [CC13](CC13-Replace-The-Update-Pipeline-Python-Tools.md) | blocked | Sokar B53 | The Python tools the update job runs, and the per-push digest check, replaced by the tool Sokar publishes. | 0 |
| [CC14](CC14-Acceptance-As-Kit-Scenarios.md) | blocked | Sokar B53 | The acceptance shell script turned into scenarios on acceptance-kit steps. | 1 |
| [CC01](CC01-Pin-GitHub-Actions-By-Sha.md) | handed on | — | Every third-party GitHub Action runs from a mutable tag, beside the tokens that publish packages and open pull requests. | 1 |
| [CC04](CC04-Automated-Agent-Updates.md) | open | — | The update pipeline is built; what it still decides by convention rather than by a stated rule. | 4 |
| [CC05](CC05-Declare-What-Waiting-Looks-Like.md) | blocked | Sokar B47 | Declaring what "waiting for a person" looks like in this agent's own output. | 1 |
| [CC09](CC09-Fail-Acceptance-When-A-Release-Adds-A-Dialog.md) | blocked | Sokar B52 | The acceptance run fails when a release adds a first-run dialog. | 1 |
| [CC10](CC10-Declare-Where-The-Session-Id-Is.md) | blocked | Sokar B46 | Declaring where this agent's session id is, so a task that comes back continues its conversation. | 1 |
| [CC15](CC15-Refuse-The-Update-Host.md) | blocked | Sokar B61 | Refusing the host the CLI updates itself from, once refusals reach the resolver. | 0 |

**Status** means: `open` - nobody is on it. `in progress` - somebody is. `handed on` - the work
belongs to another repository and this row tracks what has to change here afterwards. `blocked` -
waiting on something else, and **Blocked by** names it: an issue here by its number, a Sokar
requirement as `Sokar B<n>`.

## The one that is not ours to finish

**001** is tracked centrally as Sokar requirement **B49**, because the same mutable tags carry the
same risk in every repository the four agents maintain. Its open question is the one that decides
whether pinning helps at all: what keeps the pins current, since a pin without an update process
rots silently.

## Handed over from Sokar, 2026-09-12

Five agent requirements moved here when the operator ruled that an agent's work lives in its own
repository. **A02** became the update issue above (one per agent repository rather than one shared
file), **A11** the waiting one. The per-agent requirements were met: what outlived them is in
[`doc/decisions.md`](../doc/decisions.md), and the files themselves are gone.

`A01` and the candidate agents without a repository stay in sokar, where `issues/agents/` is now
the place an agent lives before it has one.

## Where the rest of the open work lives

Not everything open is an issue. Accepted risks - exposures that are known, deliberate and not
being removed - are in [`doc/decisions.md`](../doc/decisions.md) with what would change the
answer. A finding that has been answered is neither: it is in the code, with its reasoning.
