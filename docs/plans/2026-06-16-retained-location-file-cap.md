---
title: Retained Location File Cap
date: 2026-06-16
status: planned
execution: code
---

## Context

Startup reads are limited to the 1,000 newest compatible location files, but
every successful save leaves another file on disk. Long-running use can
therefore grow app-managed journal storage and future directory enumeration
without bound.

## Requirements

- After an atomic save, retain only the 1,000 newest compatible timestamped
  location JSON files.
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
