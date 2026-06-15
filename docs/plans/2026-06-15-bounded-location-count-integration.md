---
title: Bounded Location Count Integration
date: 2026-06-15
status: completed
execution: code
---

## Context

The current location-storage stack validates file type, size, JSON, coordinates,
unique writes, and chronological publication, but it does not contain the
separate 1,000-file startup decode bound. The earlier count patch only parses
legacy `timestamp.json` names, while current writes use
`timestamp-UUID.json`; applying it unchanged would skip every new-format file.

## Requirements

- Bound startup data reads and decodes to the 1,000 newest eligible location
  files.
- Parse timestamps from both legacy and current unique JSON filenames.
- Select equal-timestamp candidates deterministically by their unique filename.
- Preserve regular-file, 64 KiB, JSON, coordinate, and chronological ordering
  guardrails.
- Leave older files on disk and do not claim directory enumeration is bounded.
- Add mutation-sensitive static contracts and synchronized documentation.

## Non-Goals

- Deleting or migrating persisted files.
- Changing save filenames, notification behavior, or map/table presentation.
- Modernizing the legacy Swift or Xcode project.
- Claiming simulator, device, or persisted-data execution from Linux.

## Verification Plan

- Run Python syntax checks, all four Make gates, and the external-directory Make
  gate.
- Reject isolated count, legacy-name, unique-name, newest-first, equal-timestamp
  tie-break, prefix-before-read, chronological-order, documentation, and
  plan-evidence mutations.
- Audit the exact diff, generated artifacts, project/workflow files, binaries,
  whitespace, conflict markers, and changed-line credential patterns.
- Capture one bounded exact-head pull-request and security snapshot after push.

## Work Completed

- Added a 1,000-file startup candidate limit after regular-file, size, and
  compatible timestamp-name validation but before any file data read.
- Accepted exact legacy timestamp stems and current timestamp-UUID stems while
  rejecting non-finite timestamps and malformed UUID suffixes.
- Selected candidates newest-first with a deterministic filename tie-break,
  decoded only the retained subset, and restored chronological location order
  after JSON and coordinate validation.
- Added ordering-sensitive static contracts and synchronized repository
  guidance without deleting older files.

## Verification Completed

- All four Make gates passed from the repository.
- The external-directory Make gate passed through the absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py` passed without retaining
  generated artifacts.
- Nine isolated hostile mutations were rejected across the count constant,
  legacy filename parsing, unique filename parsing, newest-first selection,
  equal-timestamp tie-breaking, prefix-before-read ordering, chronological
  restoration, documentation, and plan evidence.
- `git diff --check`, generated-artifact inspection, protected project/workflow
  inspection, binary review, conflict-marker review, and changed-line
  credential-pattern review passed.
- xcodebuild is unavailable on this Linux host, so simulator, device, and live
  persisted-data behavior are not claimed.
