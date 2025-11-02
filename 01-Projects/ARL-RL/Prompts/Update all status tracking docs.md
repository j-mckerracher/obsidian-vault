Now I you to comprehensively update and (if missing) create fine-grained notes for the ARL RL project.

SCOPE (paths in vault)
- 01 Projects/ARL RL/Documents
- 01 Projects/ARL RL/Job-Submission-Commands
- 01 Projects/ARL RL/Work Completed
- 01 Projects/ARL RL/Experiments.md
- 01 Projects/ARL RL/Plan.md
- 01 Projects/ARL RL/Status.md

TEMPLATES (use these files verbatim as starting points; copy, fill placeholders, prune empty fields)
- Experiments (canonical per-experiment note): 01 Projects/ARL RL/Documents/Experiment.template.md
- Job submission/run notes: 01 Projects/ARL RL/Job-Submission-Commands/Job.template.md
- Daily work logs: 01 Projects/ARL RL/Work Completed/DailyWorkLog.template.md
- Experiments summary page: 01 Projects/ARL RL/Experiments.template.md
- Project plan: 01 Projects/ARL RL/Plan.template.md
- Project status: 01 Projects/ARL RL/Status.template.md
- Documents index: 01 Projects/ARL RL/Documents/Index.template.md

GOALS
- Capture precise, reproducible, fine-grained details (what, why, how, parameters, commands, results, issues, next steps).
- Ensure every experiment, job, and work session is fully documented and cross-linked.
- Create missing notes; standardize structure; avoid duplication; preserve provenance.

GLOBAL RULES
- Do not invent facts. If unknown, add a TODO with a concrete question.
- Timestamp all edits in ISO 8601; update a “last_updated” field in YAML.
- Use Obsidian [[wikilinks]] and relative paths; prefer one canonical note per experiment.
- Keep a “Changelog” section with dated bullets for every modified file.
- Sanitize secrets/tokens; replace with {{PLACEHOLDER}}.

NAMING CONVENTIONS
- experiment_id: expt-YYYYMMDD-<short-slug>
- experiment notes saved to: 01 Projects/ARL RL/Documents/Experiments/<experiment_id>-<slug>.md (create folder if missing)
- job notes: 01 Projects/ARL RL/Job-Submission-Commands/<YYYY-MM-DD>-<experiment_id>-<short-slug>.md
- daily work log: 01 Projects/ARL RL/Work Completed/YYYY-MM/YYYY-MM-DD.md (create month folder if missing)

EXECUTION ORDER
1) Inventory
   - Scan listed paths; map experiments, jobs, daily logs, plan items, status snapshots.
   - Identify missing per-experiment or per-job notes; detect duplicates; choose canonical names.

2) Experiments
   - For each experiment referenced anywhere, create/update the canonical note under Documents/Experiments using Experiment.template.md.
   - Cross-link to jobs, work logs, plan items, and related docs.
   - Update 01 Projects/ARL RL/Experiments.md (use Experiments.template.md as the structure) with one summary row per experiment.

3) Job-Submission-Commands
   - For each experiment’s runs, create/update job notes using Job.template.md.
   - Record exact commands, scheduler/resources/env, outputs/logs, and job IDs.
   - Backlink to the experiment; list job entries in the experiment note with status/artifacts.

4) Work Completed (daily logs)
   - Create/append daily entries using DailyWorkLog.template.md under Work Completed/YYYY-MM/YYYY-MM-DD.md.

5) Plan.md
   - Update using Plan.template.md structure: Objectives, Milestones (table), Tasks by state, Risks/Mitigation, Next 3 Actions.
   - Link tasks to experiments and work logs.

6) Status.md
   - Refresh using Status.template.md: last_updated, Overall (GYR), Highlights, Blockers, Risks, Upcoming, Next Actions, KPIs.
   - Link to Plan and Experiments.

7) Documents
   - Normalize/organize content in Documents; maintain an index using Documents/Index.template.md.
   - Move ad-hoc experiment content into canonical experiment notes; leave pointer stubs where moved.

8) Cross-linking & Tags
   - Ensure consistent tags: #project/arl-rl plus topical tags (#experiment, #job, #worklog, #plan, #status).
   - Add “Related” links in YAML and a Related section in body.

DELIVERABLES SUMMARY
- Output a concise change summary: files added/updated, key changes per file, and unresolved TODOs.

QUALITY BAR
- No stale “last_updated”; all modified files have dated Changelog entries.
- Every referenced experiment has a canonical note and appears in Experiments.md.
- All jobs documented and linked; daily logs exist for recent activity.
- Plan and Status reflect current reality; notes are consistently cross-linked.