# sokar-claude-code

Runs [Claude Code](https://github.com/anthropics/claude-code) inside
[Sokar](https://github.com/sokar-ai/sokar): in a hardened container, reaching only what it needs,
with your credential kept on the machine and its work waiting for your review.

## Install

Once Sokar's package repository is set up, as Sokar's
[getting started](https://github.com/sokar-ai/sokar/blob/main/doc/getting-started.md) describes:

```
sudo apt install sokar-agent-claude      # or: sudo dnf install sokar-agent-claude
```

How to sign in, start a task, what the task reaches and what to read when it does not work:
[doc/index.md](doc/index.md).

## More

- [build.md](build.md) - building the package, and moving the pinned Claude Code version.
- [doc/decisions.md](doc/decisions.md) - why it works the way it does.

## Licence

GNU General Public License v3.0 or later. See [LICENSE](LICENSE).
