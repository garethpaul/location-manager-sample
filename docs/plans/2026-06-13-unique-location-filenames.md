# Unique Location Filenames

status: completed

## Problem

Persisted location filenames are derived only from `Date.timeIntervalSince1970`.
Two accepted locations with the same timestamp therefore target the same JSON
path: the later atomic write replaces the earlier disk record while both
locations are appended to memory and announced to observers.

## Scope

- Add a unique component to every newly persisted location filename.
- Preserve the timestamp prefix for diagnostics and keep the `.json` extension.
- Preserve atomic writes, post-write publishing, bounded loading, coordinate
  validation, and chronological decode sorting.
- Add static, documentation, completion, and hostile-mutation contracts.
- Do not claim simulator, device, Core Location, or live filesystem runtime
  verification from the Linux host.

## Verification Plan

- Run `make lint`, `make test`, `make build`, and `make check`.
- Run Python compilation, project/plist/storyboard parsing, shell-independent
  diff checks, and intended-path artifact and secret scans.
- Reject filename-uniqueness removal, extension drift, stale plan status, and
  missing verification evidence mutations.
- Take one bounded exact-head push, pull-request, and code-scanning snapshot
  after push without polling.

## Non-Goals

- Renaming existing persisted files.
- Changing location payloads, notification contents, geocoding, or retention.
- Modernizing the legacy Swift/Xcode project.

## Work Completed

- Added a UUID component after the timestamp prefix for every new location
  filename while preserving the `.json` extension.
- Added static source, documentation, plan-completion, and mutation contracts.
- Preserved atomic writes, bounded startup loading, coordinate validation,
  chronological sorting, and post-write publishing.

## Verification Completed

- `make lint`, `make test`, `make build`, and `make check` completed; all four Make gates passed against the same working tree.
- The four hostile mutations were rejected: uniqueness removal, extension
  drift, stale plan status, and missing verification evidence.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- xcodebuild was unavailable on the Linux validation host.
- No simulator, device, Core Location, or live filesystem runtime verification is claimed.
