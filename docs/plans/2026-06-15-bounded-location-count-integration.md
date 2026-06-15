---
title: Bounded Location Count Integration
date: 2026-06-15
status: planned
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
- Reject isolated count, legacy-name, unique-name, newest-first, prefix-before-
  read, chronological-order, documentation, and plan-evidence mutations.
- Audit the exact diff, generated artifacts, project/workflow files, binaries,
  whitespace, conflict markers, and changed-line credential patterns.
- Capture one bounded exact-head pull-request and security snapshot after push.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and verification.
