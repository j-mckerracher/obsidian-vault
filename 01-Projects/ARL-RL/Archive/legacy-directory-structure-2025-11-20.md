# Legacy Directory Structure (Archived 2025-11-20)

## Changes Made

As part of the Phase 3 reorganization (2025-11-20), the following directory structure changes were implemented:

### Work Completed/ → Work-Log/

**Rationale**: Consolidate work tracking into a single, chronologically organized directory structure.

**Changes**:
- **Old**: `Work Completed/` with 24 dated log files (2025-10-03 through 2025-10-25)
- **New**: `Work-Log/2025-10/` with all dated logs organized by month

**Migration**: All 24 work log files moved to `Work-Log/2025-10/` subdirectory for better chronological organization.

**Documentation Updates**:
- Updated `README.md` references
- Updated `Home.md` references
- Updated `Work-Log/Index.md` with monthly organization and weekly groupings

### Notes/ Directory

**Status**: Kept in current structure

**Rationale**: Notes/ contains only 2 files:
1. `Engineering Notes - Mixed Precision and HPC.md` — Technical documentation
2. `Index.md` — Directory index

This low file count and technical focus justifies keeping Notes/ separate from daily Work-Log entries. Notes serve as permanent technical reference material vs. chronological work tracking.

### Scripts/ → Scripts-Reference/

**Changes**: Covered in Phase 2 (see Phase 2 commit for details)

**Rationale**: Clarify these are reference copies, not executable scripts

---

## Directory Purpose Summary

| Directory | Purpose | Organization |
|-----------|---------|--------------|
| **Work-Log/** | Daily progress, completed tasks, chronological milestones | By month (`YYYY-MM/`) |
| **Notes/** | Engineering notes, technical documentation, permanent reference | Flat structure |
| **Decisions/** | Key decisions with rationale | Flat with Index |
| **Documents/** | How-to guides, SLURM docs, experiment templates | By category |
| **Scripts-Reference/** | Reference copies of SLURM scripts | Flat with README |

---

*This document explains the rationale for directory structure changes made during the 2025-11-20 reorganization.*
