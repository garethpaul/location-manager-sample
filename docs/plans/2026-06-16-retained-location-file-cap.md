---
title: Retained Location File Cap
date: 2026-06-16
status: completed
execution: code
---

## Context

Startup reads are limited to the 1,000 newest compatible location files, but
every successful save leaves another file on disk. Long-running use can
therefore grow app-managed journal storage and future directory enumeration
without bound.

## Requirements

- After an atomic save, best-effort prune compatible timestamped location JSON
  files toward the newest 1,000.
- Accept both legacy `timestamp.json` and current `timestamp-UUID.json` names
  when selecting retention candidates.
- Delete oldest candidates deterministically and leave unrelated, malformed,
  non-JSON, and non-regular documents untouched.
- Preserve successful in-memory publication even when directory inspection or
  best-effort cleanup fails.
- Add ordering-sensitive static contracts, hostile mutations, and synchronized
  privacy and retention guidance.

## Non-Goals

- Claiming a bound on unrelated documents or hostile files in the app's
  documents directory.
- Migrating existing location JSON, changing filenames, or changing UI order.
- Modernizing the legacy Swift or Xcode project.
- Claiming simulator, device, Core Location, or live filesystem execution from
  Linux.

## Verification Plan

- Run Python syntax checks, all four Make aliases, and the external-directory
  Make gate.
- Reject isolated mutations for cleanup omission, wrong retention direction,
  deleting unrelated files, pruning before a successful write, cleanup failure
  blocking publication, incomplete plan evidence, and missing guidance.
- Audit the exact diff, generated artifacts, project/workflow files, binaries,
  whitespace, conflict markers, and changed-line credential patterns.
- Capture one bounded exact-head pull-request and security snapshot after push.

## Work Completed

- Added best-effort post-write pruning for regular JSON files with compatible
  legacy or timestamp-UUID location filenames.
- Reused the startup timestamp parser and newest-first filename tie-break so
  retention keeps the same deterministic 1,000-file boundary as startup reads.
- Kept cleanup after atomic persistence and before in-memory publication; a
  directory-listing or individual deletion failure returns from cleanup only,
  so the 1,000-file target is not overstated as a hard guarantee.
- Added ordering-sensitive static checks and synchronized retention and privacy
  guidance.

## Verification Completed

- All four Make gates passed through the static baseline.
- The external-directory Make gate passed through the absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py` passed with bytecode
  redirected outside the repository.
- Seven isolated hostile mutations were rejected: cleanup omission, oldest-
  first reversal, unrelated-file filter removal, pruning before the atomic
  write, cleanup failure blocking publication, incomplete plan evidence, and
  missing retention guidance.
- `git diff --check`, generated-artifact inspection, project/workflow review,
  binary inspection, conflict-marker review, and changed-line credential-pattern
  review passed.
- xcodebuild is unavailable on this Linux host, so simulator, device, Core
  Location, and live persisted-filesystem behavior are not claimed.
