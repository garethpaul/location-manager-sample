---
title: Enforce the location file size limit at save time
type: reliability
date: 2026-06-17
status: in_progress
execution: code
---

# Enforce the location file size limit at save time

## Goal

Prevent newly encoded location records from creating oversized files that sit
outside both startup loading and retained-file pruning.

## Requirements

- Reject encoded location data larger than the existing 64 KiB file limit.
- Apply the size guard before filename generation, disk writes, pruning, or
  in-memory publication.
- Preserve coordinate validation, atomic writes, successful-save pruning,
  chronological publication, notifications, and the existing file limit.
- Extend the maintained checker and guidance with mutation-sensitive contracts
  for the exact bound, ordering, documentation, and completed evidence.

## Key Technical Decisions

- Reuse `maximumLocationFileSize` so startup, pruning, and save eligibility
  cannot drift to separate numeric limits.
- Guard the encoded `Data.count` rather than estimating the input string size;
  the persisted representation is the storage boundary that matters.
- Preserve the existing no-result behavior for rejected saves: no file, prune,
  in-memory insertion, or notification is produced.

## Implementation Units

### U1. Save-time encoded-size guard

**File:** `Journal/LocationsStorage.swift`

Require encoded data to fit the shared file-size limit before constructing the
destination URL or executing any successful-save side effect.

### U2. Maintained regression contract

**Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, and this plan

Protect the shared limit comparison, save ordering, repository guidance, and
truthful completed-plan evidence against isolated weakening.

## Verification Strategy

- Run all maintained Make aliases from the repository root and the absolute
  Makefile gate from `/tmp` with the truthful Linux Xcode boundary.
- Reject isolated hostile mutations to the data-count guard, shared limit,
  ordering before filename/write/publication, documentation, and plan status.
- Audit Python and shell syntax, the exact intended diff, generated artifacts,
  file modes, conflict markers, and credential-like additions before commit.

## Scope Boundaries

- Do not change the 64 KiB or 1,000-file limits, startup decoding, retention
  ordering, compatible filenames, deletion policy, Core Location, geocoding,
  notifications, dependencies, deployment targets, or UI tests.
- Do not claim Xcode, simulator/device, live filesystem, Core Location, or
  reverse-geocoding execution from Linux.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and validation.
