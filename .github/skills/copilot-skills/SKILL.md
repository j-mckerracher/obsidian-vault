---
name: copilot-skills
description: Detailed reference for GitHub Copilot agent skills — what they are, how to create them, how Copilot invokes them, supported locations, SKILL.md format, allowed-tools, scripts, and CLI management commands. Use when asked about creating, editing, or managing Copilot skills.
---

Agent skills are folders of instructions, scripts, and resources that Copilot loads when relevant to improve its performance on specialized tasks. They follow the open [Agent Skills specification](https://github.com/agentskills/agentskills) and work with the **GitHub Copilot CLI**, the **Copilot cloud agent**, and **agent mode in VS Code**.

---

## 1. Skill storage locations

| Scope | Supported paths | Notes |
|---|---|---|
| **Project** (single repo) | `.github/skills/<skill-name>/` | `.claude/skills/` and `.agents/skills/` also work |
| **Personal** (all projects) | `~/.copilot/skills/<skill-name>/` | `~/.claude/skills/` and `~/.agents/skills/` also work |
| **Organization / Enterprise** | _(coming soon)_ | Not yet available |

Each skill lives in its **own subdirectory**. The subdirectory name should be lowercase with hyphens (e.g., `my-new-skill`).

---

## 2. SKILL.md format

Every skill requires a `SKILL.md` file (exactly that name) inside its directory. The file is **Markdown with YAML frontmatter**.

```markdown
---
name: my-skill-name          # required — lowercase, hyphens for spaces
description: >               # required — tells Copilot WHEN to invoke this skill
  One or two sentences explaining what this skill does and when to use it.
license: MIT                 # optional — license for the skill
allowed-tools:               # optional — pre-approve tools without per-use confirmation
  - shell
---

# Skill body

Markdown instructions, guidelines, tables, and examples go here.
Copilot receives this entire body as additional context when the skill is active.
```

### Frontmatter fields

| Field | Required | Description |
|---|---|---|
| `name` | ✅ | Unique identifier. Must match the directory name. Lowercase + hyphens only. |
| `description` | ✅ | Natural-language description. Copilot uses this to decide when to load the skill. Be specific about trigger conditions. |
| `license` | ❌ | Any license string (e.g., `MIT`, `Apache-2.0`). |
| `allowed-tools` | ❌ | List of tools Copilot may run without asking for confirmation. See §4. |

---

## 3. How Copilot invokes a skill

- Copilot reads every skill's `description` field at session start.
- When a user prompt matches, Copilot **injects the full `SKILL.md` body** into its context.
- All other files in the skill directory (scripts, data files, examples) are also made available.
- To **force** a specific skill, reference it by name with a leading slash:
  ```
  Use the /my-skill-name skill to ...
  ```

---

## 4. Including scripts and resources

Place any supporting files (scripts, JSON, examples) alongside `SKILL.md` in the same directory:

```
.github/skills/my-skill/
├── SKILL.md
├── run-check.sh
└── examples/
    └── sample-config.json
```

Reference them by name in the `SKILL.md` body:
```markdown
Run `run-check.sh` from this skill's base directory, passing the target path as $1.
```

### `allowed-tools` — pre-approving shell execution

```yaml
allowed-tools:
  - shell    # or: bash
```

> ⚠️ **Security warning:** Only add `shell`/`bash` to `allowed-tools` if you fully trust the skill source. Pre-approving removes the confirmation prompt, enabling arbitrary command execution. For untrusted or community skills, omit this field.

---

## 5. CLI management commands

| Command | Effect |
|---|---|
| `/skills list` or "What skills do you have?" | List all available skills |
| `/skills` | Interactive toggle — enable/disable individual skills |
| `/skills info` | Show details and file location for each skill |
| `/skills add <path>` | Add an additional skills search directory |
| `/skills reload` | Reload skills without restarting the CLI session |
| `/skills remove <skill-dir>` | Remove a directly-added skill (not plugin-managed) |

---

## 6. Skills vs. custom instructions

| | Skills | Custom instructions |
|---|---|---|
| **When loaded** | Only when relevant to the prompt | Always |
| **Best for** | Detailed, task-specific procedures | General coding standards, repo-wide conventions |
| **Location** | `.github/skills/` or `~/.copilot/skills/` | `.github/copilot-instructions.md` |
| **Invocation** | Automatic (by description match) or `/skill-name` | Implicit — always in context |

Use custom instructions for things like "always use type hints in Python." Use skills for things like "here is our 10-step deployment checklist."

---

## 7. Community skill resources

- [`anthropics/skills`](https://github.com/anthropics/skills) — Official Anthropic skill library
- [`github/awesome-copilot`](https://github.com/github/awesome-copilot) — Community-curated skills and prompts
- [Agent Skills open standard](https://github.com/agentskills/agentskills) — Specification used by Copilot, Claude, and other AI systems

---

## 8. Quick-start checklist

1. Choose a location: `.github/skills/` (project) or `~/.copilot/skills/` (personal)
2. Create a directory: `<location>/<skill-name>/` (lowercase, hyphens)
3. Create `SKILL.md` with `name`, `description`, and body instructions
4. Add any scripts or reference files to the same directory
5. Reload in an active CLI session with `/skills reload`
6. Verify with `/skills list` — your skill should appear
7. Test by prompting Copilot with a task that matches the description, or invoke explicitly with `/your-skill-name`
