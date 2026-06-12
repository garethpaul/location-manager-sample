# Bounded Location Loads

status: completed

## Problem

Persisted files are filtered by `.json` extension, but the loader accepts
non-regular files, unbounded file sizes, and decoded latitude/longitude values
outside Core Location's valid coordinate range.

## Scope

- Load only regular persisted JSON files.
- Reject files larger than 64 KiB before reading them into memory.
- Reject decoded locations with invalid or non-finite coordinates.
- Preserve corrupted-file skipping, chronological sorting, and atomic writes.
- Add static and mutation guardrails without accessing user location data in CI.

## Verification Completed

- Local `make check`, `make lint`, `make test`, and `make build` passed. The
  local environment did not provide `xcodebuild`, so these runs exercised the
  complete static baseline and reported the hosted Xcode requirement.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Hostile mutations changing the plan status, inserting an unfinished-work
  marker, falsifying a run ID, removing the 64 KiB limit, or removing coordinate
  validation were rejected.
- The main-branch push Check run `27287434242` completed successfully for
  commit `6f9a8f1ec70fab6c08b5920c4cd3544dd0a59760`.
- The CodeQL setup run `27402324815` completed successfully for commit
  `6f9a8f1ec70fab6c08b5920c4cd3544dd0a59760`.
- Loading preserves `resourceValues.isRegularFile == true`,
  `fileSize <= LocationsStorage.maximumLocationFileSize`, and
  `CLLocationCoordinate2DIsValid(location.coordinates)` before accepting data.

## Work Completed

- Added a 64 KiB maximum for persisted location JSON files.
- Required regular files and checked size metadata before reading file data.
- Rejected decoded locations unless `CLLocationCoordinate2DIsValid` accepts
  their coordinates.
- Extended static baseline and mutation checks for both input boundaries.
- Documented the local persistence boundary in project, security, vision, and
  change documentation.
