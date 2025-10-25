---
project: ARL RL
tags: [project/arl-rl, guide, llm]
created: 2025-10-05
---

# LLM Collaboration Guide — ARL RL

Purpose
- Provide clear, consistent instructions for any LLM assisting on this project about how, what, when, where, and why to document work in this Obsidian vault.
- Ensure every new piece of information shared with the LLM is captured as durable knowledge and linked to relevant artifacts (code, runs, logs, decisions).

Quickstart onboarding (≈5 minutes)
1) Open [[Status|Status.md]] and read:
   - Current best parameter set
   - Next actions and risks
2) Open [[Decisions/Index|Decisions Index]] and skim the most recent three decisions:
   - LR=0.00005 (Sweep A)
   - EPS_DECAY=20000 (Sweep B)
   - TARGET_UPDATE_FREQ=200 (Sweep C)
3) Open [[Experiments|Experiments hub]] and scan the Summary table; open the top-performing runs.
4) Note key paths and environment:
   - SAVE_PATH (default): /depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/results_split_advanced
   - LOG_DIR (default): /depot/sbagchi/data/josh/RL/FindAndDefeatZerglings/logs
   - SC2PATH (HPC): /home/jmckerra/StarCraftII
5) For confirmations, run: `bash scripts/confirm_best.sh --res 32` (overrides allowed via env).
6) After any run/decision/fix, document immediately per this guide (runs → Experiments; choices → Decisions; fixes/changes → Work Completed; update Status).

Project snapshot (context a new LLM needs immediately)
- Objective: Part 1 improve win rate via parameter-only changes; Part 2 fix NO_OP idling (targeted action-selection tweaks).
- Environment: Purdue Gilbreth HPC (Linux), NVIDIA A30 GPUs (shared). Headless SC2 4.10.
- Map: FindAndDefeatZerglings.
- Current best parameter set to validate (from sweeps):
  - LR=0.00005, EPS_DECAY=20000, TARGET_UPDATE_FREQ=200, BATCH_SIZE=8, REPLAY_MEMORY_SIZE=50000,
    SCREEN_RES=32, MINIMAP_RES=32, STEP_MUL=8.
- Key files & scripts:
  - training_split.py (env overrides, train-from-scratch path, NO_OP gating fix, JSON results & logging)
  - scripts/sweep_lr.sh, scripts/sweep_eps_decay.sh, scripts/sweep_tuf.sh (baked defaults, append CSV)
  - scripts/confirm_best.sh (3000-episode confirmations, seeds 4 & 6)
  - tools/aggregate_results.py (roll-up summary)
- Artifacts per run:
  - SAVE_PATH/RL_RUN_ID/{config.json, eval/test_results.json, train.log, checkpoints, training_curves.png}
  - LOG_DIR/RL_RUN_ID.log (structured logging from training_split.py)
- Known pitfalls addressed:
  - GPU OOM under contention → use small batch/resolution; PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
  - JSON int64 serialization → cast to builtin int/float
  - Prior script gated on final checkpoint → now trains from scratch if none found

RL_* variable glossary (common, overridable)
- RL_SAVE_PATH: Root directory for run artifacts.
- RL_LOG_DIR: Central directory for per-run .log files.
- RL_RUN_ID: Unique run identifier (recommended: UTC timestamp + label).
- RL_NUM_EPISODES / RL_START_EPISODE: Training episode counts/start.
- RL_BATCH_SIZE: Training batch size.
- RL_SCREEN_RES / RL_MINIMAP_RES: Feature map resolutions.
- RL_REPLAY_MEMORY_SIZE: Replay buffer size.
- RL_EPS_START / RL_EPS_END / RL_EPS_DECAY: Epsilon-greedy schedule.
- RL_LEARNING_RATE: Optimizer learning rate.
- RL_TARGET_UPDATE_FREQ: Target network update cadence (episodes).
- RL_STEP_MUL: SC2 step multiplier.
- RL_SEED: Random seed for reproducibility.
- SC2PATH: StarCraft II installation path (Linux HPC).
- PYTORCH_CUDA_ALLOC_CONF: Memory allocator tuning (e.g., expandable_segments:True).
- CUDA_VISIBLE_DEVICES: GPU selection (empty to force CPU).

Essential commands (quick reference)
- Confirm best parameters (3000 episodes, seeds 4 & 6):
  `bash scripts/confirm_best.sh --res 32`
- Sweeps (32×32 by default; override with --res 64 if headroom):
  - LR: `bash scripts/sweep_lr.sh --res 32`
  - Epsilon decay: `bash scripts/sweep_eps_decay.sh --res 32`
  - Target update freq: `bash scripts/sweep_tuf.sh --res 32`

Core principles
- Be immediate: Document as you go. Add or update notes right after a run, decision, bug, or code change.
- Be specific: Include exact parameters, seeds, file paths, commands, timestamps (UTC), hardware, and artifacts.
- Be linked: Cross-link related pages (runs ↔ decisions ↔ issues ↔ status). Update indexes/summary tables.
- Be minimal yet complete: Capture the facts and outcomes first; add interpretation only when helpful.
- Be reproducible: Prefer recorded env vars, configs, run IDs, and commands over narrative only.
- Be safe: Never include secrets in plaintext. Use placeholders like {{SECRET_NAME}}.

What to document
- Runs and sweeps
  - Parameters (RL_* env vars), seed(s), resolution, episodes, LR, epsilon schedule, TUF, replay size, step_mul.
  - Artifacts: run directory, config.json, eval/test_results.json, train.log, central log file path, checkpoints, plots.
  - Results: 100-episode test win rate, average reward, wins/episodes.
  - Observations: anomalies (OOM, crashes), behavior (NO_OP/attack), timing/perf notes.
- Decisions
  - Each selection (e.g., LR, EPS_DECAY, TARGET_UPDATE_FREQ) gets a dated Decision page.
  - Context (alternatives considered), rationale (why chosen), and next actions.
- Issues and fixes
  - Problem → root cause → solution → result, with snippets of error messages and affected files.
- Code changes
  - What changed, where (path), why, and any side effects. Link to related runs/decisions.
- Status/progress
  - High-level summary of where we are, recent results, current best params, next actions, and risks.

When to document
- Immediately after:
  - Running a training/test (single run or sweep)
  - Making a decision (parameter choice, process change)
  - Encountering an issue and applying a fix
  - Modifying code or scripts
  - Changing the plan or success criteria
- Daily/periodic:
  - Update Status with major outcomes and what’s next
  - Ensure Experiments summary table and Decisions index are current

Where to document (folder and page mapping)
- Experiments
  - Experiments.md (hub): Summary table of all runs with links
  - Experiments/TEMPLATE.md: Use as the structure for per-run pages
  - Experiments/[run_id].md: Per-run details (config deltas, metadata, results, observations)
- Decisions
  - Decisions/[YYYY-MM-DD] Title.md: One file per decision with context and rationale
  - Decisions/Index.md: List and link all decision files (latest first)
- Work Completed
  - Work Completed/[YYYY-MM-DD] Title.md: Logs of code changes, issues and solutions
  - Work Completed/Index.md: List and link key work logs
- Status
  - Status.md: Overall project status, current best parameters, next actions, risks
- Plan
  - Experiments/Plan.md: Procedural plan for sweeps and confirmations
- References
  - This guide and other process/reference docs

How to document (mechanics and conventions)
- Identify runs with RL_RUN_ID and use it in per-run page titles and summary table entries
  - Example RL_RUN_ID: 20251005_070524_sweepC_tuf_200
- Always include:
  - UTC timestamp(s) (e.g., 2025-10-05T08:05:55Z)
  - Exact RL_* env vars used or “not_set” when defaults applied
  - Hardware/GPU notes when relevant (e.g., NVIDIA A30)
  - Paths: SAVE_PATH, LOG_DIR, artifacts
- Keep indexes in sync:
  - Append the run to Experiments.md summary table with link and win rate
  - Add new decisions to Decisions/Index.md
  - Add significant work logs to Work Completed/Index.md
- Cross-link related material:
  - From runs to decisions (“Decision: LR=5e-5”), to issues (“OOM fix”), and back to Status
- Use consistent naming:
  - Files: [YYYY-MM-DD] Title.md for decisions/work logs; [run_id].md for runs
  - Commit messages (for this vault): [YYYY-MM-DD HH:MM UTC] Short, human-readable description
- Capture unknowns explicitly:
  - If a value is unknown, write “unknown” or “not_set” and add a short TODO for follow-up
- Secrets and tokens:
  - Never store secrets in plaintext. Use {{SECRET_NAME}} placeholder and reference the secret manager process

Why this process matters
- Reproducibility: Anyone (human or LLM) can reconstruct runs and decisions
- Velocity: Fewer repeated investigations; quick identification of the best parameters
- Reliability: Structured logging of issues and fixes prevents regressions
- Collaboration: Consistent organization and cross-links reduce context-switching costs

LLM action checklist (each time you assist)
- Before executing work:
  - Check Status.md for current best parameters and pending actions
  - Review Decisions/Index.md for recent choices that affect your task
- After executing work (run, fix, or code change):
  - Create/update a per-run page in Experiments and add it to the summary table
  - If you made or solidified a choice, add a Decision page and link it in the index
  - If you fixed or investigated an issue, add a Work Completed log entry
  - Update Status.md if the overall picture changed
  - Ensure all pages have correct links to artifacts and logs
- Verification:
  - Confirm that eval/test_results.json exists for runs and sweep CSVs were updated (if applicable)
  - Confirm that central log file (RL_LOG_DIR) contains the run’s log

Templates and snippets
- Per-run page: copy from Experiments/TEMPLATE.md
- Decision pages: include context, alternatives, rationale, next actions
- Work logs: problem → root cause → solution → result

Escalation and edge cases
- If a required folder/file is missing, create it with a minimal stub and link it
- If a step would duplicate content, prefer to link existing material and add a brief delta note
- If unsure where something belongs, place it under Notes with a TODO to relocate, and mention it in Status

Maintenance
- Periodically reconcile:
  - Experiments summary table vs. actual run pages
  - Decision notes vs. what the code/scripts currently use
  - Status content vs. latest results and planned next steps

End of guide.
