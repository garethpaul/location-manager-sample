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

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- mutation checks for file-size and coordinate validation
- `git diff --check`

## Work Completed

- Added a 64 KiB maximum for persisted location JSON files.
- Required regular files and checked size metadata before reading file data.
- Rejected decoded locations unless `CLLocationCoordinate2DIsValid` accepts
  their coordinates.
- Extended static baseline and mutation checks for both input boundaries.
- Documented the local persistence boundary in project, security, vision, and
  change documentation.
