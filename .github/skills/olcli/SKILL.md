---
name: olcli
description: >
  Comprehensive reference for olcli — the Overleaf CLI tool for syncing, managing, and compiling LaTeX projects from the terminal.
  Use this skill when asked to interact with Overleaf projects from the command line: listing projects, pulling/pushing/syncing files,
  compiling PDFs, uploading figures, downloading output artifacts (bbl, log, aux), preparing arXiv submissions, or setting up
  Git + Overleaf workflows.
allowed-tools: shell
---

Use this skill whenever you need to interact with Overleaf projects via the terminal using the `olcli` command.
All operations go through the Overleaf API using a session cookie for authentication.

Run `olcli --version` or `npx @aloth/olcli --version` to confirm the tool is available.

---

## 1. Installation

### Preferred (global, persistent)
```bash
npm install -g @aloth/olcli
```

### macOS/Linux via Homebrew
```bash
brew tap aloth/tap
brew install olcli
```

### No-install (one-off use)
```bash
npx @aloth/olcli list
```

Verify install:
```bash
olcli --version
olcli check        # shows config paths and credential resolution order
```

---

## 2. Authentication

olcli uses Overleaf's browser session cookie — **no password is stored**.

### Getting the cookie
1. Log into [overleaf.com](https://www.overleaf.com) in a browser.
2. Open DevTools (F12 or Cmd+Option+I) → Application/Storage → Cookies → `overleaf.com`.
3. Copy the value of the `overleaf_session2` cookie.

### Storing the cookie
```bash
olcli auth --cookie "s%3AyourSessionCookieValue..."
```

The cookie is saved to `~/.config/olcli-nodejs/config.json`.

### Check who is authenticated
```bash
olcli whoami
```

### Clear credentials
```bash
olcli logout
```

### Credential resolution order (highest to lowest priority)
| Priority | Source |
|----------|--------|
| 1 | `OVERLEAF_SESSION` environment variable |
| 2 | `.olauth` file in current directory |
| 3 | `~/.config/olcli-nodejs/config.json` global config |

### Per-project credentials (`.olauth` file)
Create a `.olauth` file in the project directory containing **only** the raw cookie value:
```
s%3AyourSessionCookieValue...
```
Add `.olauth` to `.gitignore` — never commit credentials.

### CI/CD / automation
```bash
export OVERLEAF_SESSION="s%3AyourSessionCookieValue..."
olcli list
```

### Session expiry
Cookies stay valid for weeks. If you get 401/auth errors, refresh by grabbing a new cookie from the browser and re-running `olcli auth`.

---

## 3. Project Discovery

```bash
olcli list                     # list all projects (name, ID, last modified)
olcli list --json              # machine-readable JSON output
olcli info                     # show details + file list for auto-detected project
olcli info "My Thesis"         # show details for a named project
```

Auto-detection: any directory containing `.olcli.json` is recognized as a project directory. Most commands that accept `[project]` will auto-detect when run from such a directory.

---

## 4. Pull (Download Project Locally)

```bash
# Basic pull — creates a directory named after the project
olcli pull "Research Paper"

# Pull into a specific directory
olcli pull "My Thesis" thesis/

# Pull from project directory (auto-detect)
olcli pull
```

### Pull behavior
- Downloads all files from Overleaf.
- **Skips** local files modified after the last pull timestamp — will NOT overwrite local work.
- Creates `.olcli.json` in the directory to record project ID and last-sync timestamp.

### Force overwrite
```bash
olcli pull --force             # overwrite local changes with remote versions
```

---

## 5. Push (Upload Local Changes)

```bash
# Push from a synced directory (auto-detect)
olcli push

# Push from explicit directory
olcli push ./thesis/

# Preview what would be pushed
olcli push --dry-run

# Upload every file (not just modified-since-last-pull)
olcli push --all
```

### Push behavior
- Uploads files modified after the last pull timestamp.
- `--all` ignores the timestamp filter and uploads everything.
- `--dry-run` prints what would be uploaded without sending anything.

---

## 6. Sync (Bidirectional)

```bash
olcli sync                     # pull remote changes, then push local changes
olcli sync ./thesis/           # sync a specific directory
olcli sync --verbose           # show per-file operations
```

### Sync behavior
1. Pulls remote changes (skipping locally modified files — local wins if newer).
2. Pushes local changes back to remote.

Use `sync` for the day-to-day workflow when collaborating: remote and local both accumulate changes.

---

## 7. Compile and PDF

```bash
# Trigger compilation only (no download)
olcli compile
olcli compile "Conference Paper"

# Compile and download PDF to current directory
olcli pdf
olcli pdf "My Thesis"
olcli pdf -o draft.pdf                   # save with a custom filename
olcli pdf "Conference Paper" -o paper.pdf
```

Compilation runs on Overleaf's remote LaTeX engine — the same compiler used by the web editor.

---

## 8. File Upload and Download

### Upload a single file
```bash
olcli upload figures/diagram.png                  # into auto-detected project
olcli upload figures/diagram.png "My Paper"       # into a named project
```

### Download a single file
```bash
olcli download main.tex                           # from auto-detected project
olcli download main.tex "My Paper"                # from named project
```

### Download entire project as zip
```bash
olcli zip                                         # auto-detect project
olcli zip "My Thesis"                             # named project
olcli zip "My Thesis" -o backup.zip              # custom output filename
```

---

## 9. Compile Output Artifacts

Use `olcli output` to retrieve auxiliary files produced during compilation (essential for arXiv submissions).

```bash
# List all available output files
olcli output --list
# Example output:
#   aux          output.aux
#   bbl          output.bbl
#   blg          output.blg
#   log          output.log

# Download a specific artifact by type
olcli output bbl                                  # downloads .bbl file
olcli output log                                  # downloads compilation log
olcli output aux                                  # downloads .aux file

# Download with custom filename
olcli output bbl -o main.bbl
olcli output bbl --project "My Paper" -o main.bbl
```

---

## 10. Diagnostics

```bash
olcli check        # show resolved config paths and credential source
olcli whoami       # confirm authenticated identity
```

---

## 11. Common Workflows

### Initial setup for a project
```bash
olcli auth --cookie "s%3A..."        # one-time auth
olcli list                           # find your project name
olcli pull "My Project" my-project/
cd my-project/
```

### Daily editing loop
```bash
# Edit .tex files with any editor
vim main.tex

# Sync with Overleaf (bidirectional)
olcli sync

# Compile and preview PDF
olcli pdf -o draft.pdf
```

### Git + Overleaf workflow
```bash
# Import project into Git
olcli pull "My Thesis" thesis/
cd thesis/
git init && git add . && git commit -m "Initial import from Overleaf"

# Daily workflow
vim chapters/methods.tex
git add -A && git commit -m "Draft methods section"
olcli sync                           # keep Overleaf in sync
olcli pdf -o draft.pdf
```

### Prepare arXiv submission
```bash
cd my-paper/
olcli compile                        # ensure latest build artifacts exist
olcli output bbl -o main.bbl         # download bibliography for arXiv
olcli zip -o arxiv-submission.zip    # package all source files
```

### CI/CD pipeline
```bash
#!/bin/bash
set -euo pipefail
export OVERLEAF_SESSION="$OVERLEAF_SESSION_SECRET"
olcli pull "Automated Report" report/
cd report/
./generate-data.py > tables/results.tex
olcli push
olcli pdf -o "report-$(date +%Y-%m-%d).pdf"
```

### Backup all projects
```bash
mkdir -p backups/
for proj in $(olcli list --json | jq -r '.[].name'); do
  olcli zip "$proj" -o "backups/${proj}.zip"
  echo "Backed up: $proj"
done
```

---

## 12. Command Reference

| Command | Arguments | Flags | Description |
|---------|-----------|-------|-------------|
| `olcli auth` | — | `--cookie <val>` | Store session cookie |
| `olcli whoami` | — | — | Check authentication status |
| `olcli logout` | — | — | Clear stored credentials |
| `olcli check` | — | — | Show config paths and credential resolution |
| `olcli list` | — | `--json` | List all Overleaf projects |
| `olcli info` | `[project]` | — | Show project details and file list |
| `olcli pull` | `[project] [dir]` | `--force` | Download project files locally |
| `olcli push` | `[dir]` | `--all`, `--dry-run` | Upload local changes to Overleaf |
| `olcli sync` | `[dir]` | `--verbose` | Bidirectional sync (pull + push) |
| `olcli upload` | `<file> [project]` | — | Upload a single file |
| `olcli download` | `<file> [project]` | — | Download a single file |
| `olcli zip` | `[project]` | `-o <file>` | Download project as zip archive |
| `olcli compile` | `[project]` | — | Trigger remote PDF compilation |
| `olcli pdf` | `[project]` | `-o <file>` | Compile and download PDF |
| `olcli output` | `[type]` | `--list`, `-o <file>`, `--project <name>` | Download compile artifact |

---

## 13. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` / auth error | Session cookie expired | Grab a fresh `overleaf_session2` cookie from browser and run `olcli auth` again |
| Pull skips a local file you want updated | Local file is newer than last pull | Run `olcli pull --force` to overwrite |
| Push uploads nothing | No files modified since last pull | Run `olcli push --all` to force upload everything |
| Compile fails | LaTeX errors in source | Check Overleaf web editor for full error log; run `olcli output log` for compilation log |
| Missing `.bbl` / aux output | Project not yet compiled | Run `olcli compile` first, then `olcli output bbl` |
| `olcli: command not found` | Not installed globally | Use `npx @aloth/olcli <command>` or run `npm install -g @aloth/olcli` |
| Wrong project detected | Running from wrong directory | Pass project name explicitly: `olcli pull "My Project"` or `cd` to correct directory |
| `.olcli.json` missing | Directory not initialized | Run `olcli pull "<project>"` from that directory to initialize it |

---

## 14. Files and Directories

| Path | Purpose |
|------|---------|
| `.olcli.json` | Per-project metadata: project ID, last sync timestamp. Created by `pull`. |
| `.olauth` | Per-project session cookie (overrides global config). Add to `.gitignore`. |
| `~/.config/olcli-nodejs/config.json` | Global credential store (macOS/Linux). |
| `OVERLEAF_SESSION` | Env var for credentials in CI/scripting (highest priority). |

---

## 15. Notes and Constraints

- **olcli does not manage Overleaf accounts or billing** — it only accesses projects the authenticated user can see.
- **Overleaf Free tier** may have compilation limits; compilation errors on free plans may silently fall back to a cached PDF.
- **Conflict resolution is timestamp-based**: the newer file wins in both pull and sync. There is no three-way merge — manual resolution may be needed for true conflicts.
- **Binary files** (images, fonts, PDFs included as assets) are uploaded/downloaded as-is.
- **Large projects** with many files may take time on the first pull; subsequent syncs are fast (incremental).
- **The `overleaf_session2` cookie** is sensitive — treat it like a password. Never commit `.olauth` to source control.
