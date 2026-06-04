---
name: github-cli
description: Comprehensive reference for the GitHub CLI (gh). Use this skill when asked to perform any GitHub operation from the command line — creating or managing issues, pull requests, repositories, releases, GitHub Actions workflows, searches, or raw API calls using gh.
---

Use this skill whenever you need to interact with GitHub from the terminal. All commands use the `gh` binary. Run `gh --version` to confirm it is installed.

## 1. Authentication

| Goal | Command |
|---|---|
| Log in interactively | `gh auth login` |
| Log in for GitHub Enterprise | `gh auth login --hostname <hostname>` |
| Check auth status | `gh auth status` |
| Print current token | `gh auth token` |
| Log out | `gh auth logout` |
| Refresh scopes | `gh auth refresh --scopes repo,write:packages` |
| Configure git to use gh credentials | `gh auth setup-git` |

**Non-interactive / scripting auth:**
```bash
# Set token via environment variable (takes precedence over stored credentials)
export GITHUB_TOKEN=<token>

# For GitHub Enterprise
export GH_HOST=github.mycompany.com
export GH_ENTERPRISE_TOKEN=<token>
```

## 2. Configuration

```bash
gh config list                          # show all settings
gh config get editor                    # get a single setting
gh config set editor "code --wait"      # set preferred editor
gh config set git_protocol ssh          # use ssh instead of https
gh config clear-cache                   # clear cached responses
```

**Key environment variables:**

| Variable | Purpose |
|---|---|
| `GITHUB_TOKEN` | Auth token, overrides stored credentials |
| `GH_TOKEN` | Alias for `GITHUB_TOKEN` |
| `GH_HOST` | Default GitHub hostname (for GHE) |
| `GH_REPO` | Override repo context (`OWNER/REPO`) |
| `GH_EDITOR` | Editor for writing bodies |
| `GH_BROWSER` | Browser for `--web` flags |
| `NO_COLOR` | Disable color output |

## 3. Repositories

```bash
# Create
gh repo create my-repo --public --clone
gh repo create org/my-repo --private --description "My repo"
gh repo create --template owner/template-repo

# Clone
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1      # pass git flags after --

# Fork
gh repo fork owner/repo --clone           # fork and clone
gh repo fork --remote=true                # inside a repo; adds upstream remote

# View / edit
gh repo view                              # current repo in terminal
gh repo view owner/repo --web             # open in browser
gh repo edit --visibility private
gh repo edit --enable-wiki=false --delete-branch-on-merge

# Sync / rename / archive
gh repo sync                              # sync fork with upstream
gh repo rename new-name
gh repo archive owner/repo
gh repo set-default owner/repo            # set default repo for gh commands

# List repos
gh repo list --limit 50 --source         # only non-fork repos
gh repo list org --archived
```

## 4. Issues

```bash
# Create
gh issue create                                          # interactive
gh issue create --title "Bug: login fails" --body "Steps to reproduce..."
gh issue create --label bug --label critical --assignee @me
gh issue create --web                                    # open browser form

# List
gh issue list                            # open issues, default 30
gh issue list --state closed --limit 50
gh issue list --label bug --assignee @me
gh issue list --milestone v2.0 --json number,title,url

# View / edit
gh issue view 42
gh issue view 42 --web
gh issue edit 42 --add-label enhancement --remove-label bug
gh issue edit 42 --title "New title" --body "Updated body"
gh issue edit 42 --add-assignee octocat --milestone v2.0

# Manage lifecycle
gh issue close 42 --reason "not planned"
gh issue reopen 42
gh issue comment 42 --body "Looks good to me"
gh issue delete 42 --yes
gh issue pin 42
gh issue lock 42 --reason spam
gh issue transfer 42 owner/other-repo

# Create branch from issue (linked development)
gh issue develop 42 --name my-feature-branch --checkout
```

## 5. Pull Requests

```bash
# Create
gh pr create                                             # interactive
gh pr create --fill                                      # use commit info for title/body
gh pr create --title "Add feature X" --body "Closes #42"
gh pr create --draft --label work-in-progress
gh pr create --base main --head feature-branch
gh pr create --web                                       # open browser form

# List
gh pr list                               # open PRs
gh pr list --state closed --limit 20
gh pr list --author @me
gh pr list --label "needs review" --json number,title,headRefName

# Status (PRs relevant to you)
gh pr status

# View / diff
gh pr view 123
gh pr view 123 --web
gh pr diff 123

# Checkout a PR locally
gh pr checkout 123                       # by number
gh pr checkout feature-branch           # by branch name

# Review
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please address the comments"
gh pr review 123 --comment --body "LGTM overall"

# CI / checks
gh pr checks 123                         # list all check runs
gh pr checks 123 --watch                 # poll until complete

# Edit
gh pr edit 123 --title "New title" --add-label bug
gh pr edit 123 --add-reviewer octocat --add-assignee @me
gh pr edit 123 --milestone v2.0
gh pr ready 123                          # mark draft PR as ready

# Update branch
gh pr update-branch 123                  # merge base branch into PR branch
gh pr update-branch 123 --rebase

# Merge
gh pr merge 123 --squash --delete-branch
gh pr merge 123 --merge --auto           # enable auto-merge
gh pr merge 123 --rebase

# Close / revert
gh pr close 123
gh pr reopen 123
gh pr revert 123                         # create a revert PR
```

## 6. GitHub Actions

### Workflows

```bash
gh workflow list
gh workflow list --all                   # include disabled
gh workflow view ci.yml
gh workflow run ci.yml                                   # trigger manually
gh workflow run ci.yml -f env=production -f deploy=true  # with inputs
gh workflow enable ci.yml
gh workflow disable ci.yml
```

### Runs

```bash
# List
gh run list                              # recent runs, current repo
gh run list --workflow ci.yml --limit 10
gh run list --branch main --status failure

# View / watch
gh run view 12345678
gh run view 12345678 --log               # print full logs
gh run view 12345678 --log-failed        # print only failed step logs
gh run watch 12345678                    # live output until complete

# Control
gh run rerun 12345678
gh run rerun 12345678 --failed           # rerun only failed jobs
gh run cancel 12345678

# Download artifacts
gh run download 12345678                 # download all artifacts
gh run download 12345678 -n my-artifact -D ./artifacts

# Delete
gh run delete 12345678
```

### Cache

```bash
gh cache list
gh cache list --key prefix-
gh cache delete <cache-id>
gh cache delete --all                    # clear all caches for repo
```

## 7. Releases

```bash
# Create
gh release create v1.0.0
gh release create v1.0.0 --title "Version 1.0" --notes "Bug fixes and improvements"
gh release create v1.0.0 --generate-notes              # auto-generate release notes
gh release create v1.0.0 --draft
gh release create v1.0.0 --prerelease
gh release create v1.0.0 ./dist/*.tar.gz               # attach assets

# List / view
gh release list
gh release view v1.0.0
gh release view --json tagName,publishedAt,assets

# Edit
gh release edit v1.0.0 --title "v1.0.1 Patch" --draft=false

# Upload / download assets
gh release upload v1.0.0 ./myapp-linux-amd64 --clobber
gh release download v1.0.0 -A zip -D ./downloads
gh release download v1.0.0 -p "*.tar.gz"

# Verify and delete
gh release verify-asset v1.0.0 ./myapp.tar.gz
gh release delete v1.0.0 --yes --cleanup-tag
gh release delete-asset v1.0.0 myapp.zip --yes
```

## 8. Search

```bash
# Repositories
gh search repos "machine learning" --language python --stars ">1000"
gh search repos --owner myorg --archived=false

# Issues and PRs
gh search issues "memory leak" --repo cli/cli --state open
gh search issues --assignee @me --label bug
gh search prs --review-requested @me --state open

# Code
gh search code "TODO" --repo owner/repo --extension go
gh search code "func main" --language go --owner myorg

# Commits
gh search commits "fix: memory" --repo owner/repo --author @me
```

**Excluding qualifiers (PowerShell):**
```powershell
# Use --% stop-parse flag on PowerShell
gh --% search issues -- "my search query -label:bug"
```

**Excluding qualifiers (bash/zsh):**
```bash
gh search issues -- "my search query -label:bug"
```

## 9. API Access

Use `gh api` for any GitHub REST v3 or GraphQL v4 operation not covered by a subcommand.

### REST API

```bash
# GET (default)
gh api repos/{owner}/{repo}/releases
gh api repos/{owner}/{repo}/issues --jq '.[].title'

# POST / PATCH / DELETE
gh api repos/{owner}/{repo}/issues/123/comments -f body='LGTM'
gh api -X PATCH repos/{owner}/{repo}/issues/123 -f state=closed
gh api -X DELETE repos/{owner}/{repo}/issues/123/labels/bug

# Paginate all results
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].number'

# Read body from file
gh api repos/{owner}/{repo}/rulesets --input ruleset.json

# Custom headers
gh api -H 'Accept: application/vnd.github.v3.raw+json' repos/{owner}/{repo}/contents/README.md

# Cache a response for 1 hour
gh api repos/{owner}/{repo}/releases --cache 1h
```

### GraphQL API

```bash
gh api graphql -F owner='{owner}' -F name='{repo}' -f query='
  query($name: String!, $owner: String!) {
    repository(owner: $owner, name: $name) {
      issues(first: 10, states: OPEN) {
        nodes { number title }
      }
    }
  }
'

# Paginate GraphQL (query must accept $endCursor and return pageInfo)
gh api graphql --paginate -f query='
  query($endCursor: String) {
    viewer {
      repositories(first: 100, after: $endCursor) {
        nodes { nameWithOwner }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
'
```

### Output formatting

```bash
gh api repos/{owner}/{repo}/releases --jq '.[0] | {tag: .tag_name, url: .html_url}'

gh api repos/{owner}/{repo}/issues --template \
  '{{range .}}#{{.number}} {{.title}}{{"\n"}}{{end}}'
```

## 10. Additional Commands

### Browse
```bash
gh browse                                # open current repo in browser
gh browse 42                             # open issue or PR #42
gh browse --settings                     # open repo settings
gh browse --projects                     # open projects tab
```

### Gists
```bash
gh gist create script.sh --public --desc "My script"
gh gist create - <<< "inline content"
gh gist list
gh gist view <gist-id>
gh gist edit <gist-id>
gh gist clone <gist-id>
```

### Aliases
```bash
gh alias set pv 'pr view'               # gh pv 42  →  gh pr view 42
gh alias set co 'pr checkout'
gh alias list
gh alias delete pv
```

### Extensions
```bash
gh extension install owner/gh-extension-name
gh extension list
gh extension upgrade --all
gh extension remove gh-extension-name
gh extension search <keyword>
```

### Status dashboard
```bash
gh status                                # your mentions, reviews, assignments across all repos
```

### Labels
```bash
gh label list
gh label create bug --color d73a4a --description "Something isn't working"
gh label edit bug --name "type: bug"
gh label clone owner/source-repo        # copy all labels from another repo
gh label delete bug --yes
```

### Organization
```bash
gh org list                              # list organizations you belong to
```

## 11. Scripting Tips

### JSON output
Most commands support `--json` with a comma-separated list of fields:
```bash
gh pr list --json number,title,state,url
gh issue list --json number,title,labels --jq '.[] | select(.labels[].name=="bug")'
gh run list --json databaseId,name,status --jq '.[] | select(.status=="failure")'
```

### Exit codes
| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of command |
| 4 | Authentication required |

Check in scripts:
```bash
if gh pr merge 123 --squash; then
  echo "Merged successfully"
fi
```

### Targeting a specific repo
Use `-R`/`--repo` with any command or set `GH_REPO`:
```bash
gh issue list --repo owner/other-repo
GH_REPO=owner/repo gh pr list
```

### PowerShell quoting notes
- Wrap values with `{...}` in quotes: `gh api "repos/{owner}/{repo}/issues"`
- Use `--%` stop-parse for search qualifiers: `gh --% search issues -- "query -label:bug"`
- Use `--` before query strings that start with `-`

### Combining with jq
```bash
# Get the latest release tag
gh release list --json tagName,publishedAt --jq 'sort_by(.publishedAt) | last | .tagName'

# Wait for a workflow run to finish and get conclusion
gh run list --workflow ci.yml --limit 1 --json databaseId --jq '.[0].databaseId' \
  | xargs -I{} gh run watch {}
```
