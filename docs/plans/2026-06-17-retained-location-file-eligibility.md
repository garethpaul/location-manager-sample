---
title: Align retained location file eligibility
type: reliability
date: 2026-06-17
status: completed
execution: code
---

# Align retained location file eligibility

## Goal

Ensure successful-save pruning counts only the same size-eligible compatible
location JSON files that startup can read, so oversized timestamp-named files
cannot displace valid retained locations from the 1,000-file budget.

## Requirements

- Require a regular file and a known size no larger than 64 KiB before a file
  participates in retention ordering or deletion.
- Preserve timestamp and timestamp-UUID filename compatibility, newest-first
  ordering, deterministic equal-timestamp ordering, best-effort deletion, and
  successful in-memory publication.
- Leave unrelated JSON files, malformed names, directories, and oversized
  location-shaped files untouched and outside the compatible retention budget.
- Extend the maintained checker and guidance with mutation-sensitive contracts
  for size-key enumeration, size eligibility, completed plan evidence, and the
  aligned startup/retention boundary.

## Implementation Units

### U1. Retention eligibility alignment

**File:** `Journal/LocationsStorage.swift`

Request both regular-file and size metadata during pruning, then reject missing
or oversized sizes before timestamp parsing and sorting.

### U2. Maintained regression contract

**Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, and this plan

Protect the size metadata request, exact maximum-size comparison, maintained
guidance, and completed verification evidence against isolated weakening.

## Verification Strategy

- Run all maintained Make aliases from the repository and the absolute Makefile
  gate from `/tmp` with the truthful Linux Xcode boundary.
- Reject isolated mutations to size-key enumeration, file-size binding, maximum
  comparison, documentation, and completed-plan status.
- Audit the exact intended diff, Python and shell syntax, generated artifacts,
  conflict markers, file modes, and credential-like additions before commit.

## Scope Boundaries

- Do not change the 64 KiB or 1,000-file limits, startup decoding, filename
  formats, deletion error policy, save ordering, notifications, or Core Location
  behavior.
- Do not claim Xcode, simulator/device, or live persisted-filesystem execution
  from Linux.

## Work Completed

- Requested file-size metadata during successful-save pruning and excluded
  missing or oversized sizes before timestamp parsing and retention ordering.
- Kept the existing regular-file, JSON extension, compatible filename,
  newest-first ordering, deterministic tie-break, best-effort deletion, and
  publication behavior unchanged.
- Extended the maintained checker and repository guidance so startup and
  pruning share the documented 64 KiB eligibility boundary.

## Verification Completed

- All four Make gates passed from the repository root through the maintained
  static iOS baseline.
- The absolute Makefile gate passed from `/tmp`.
- Five isolated hostile mutations were rejected for size-key enumeration,
  file-size binding, maximum-size comparison, maintained guidance, and
  completed-plan status.
- Python checker syntax, exact diff, generated-artifact, conflict-marker,
  file-mode, and changed-line credential-pattern audits passed.
- `xcodebuild` is unavailable on this Linux host, so simulator/device and live
  persisted-filesystem behavior were not claimed.
