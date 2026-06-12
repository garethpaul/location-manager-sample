# Bounded Location File Count

status: completed

## Context

Persisted location loads reject non-JSON, non-regular, oversized, and malformed
files, but startup still attempts to decode every eligible file in Documents.
A large accumulated or injected journal can therefore create unbounded decode,
sorting, and in-memory location work.

## Priorities

1. Bound the number of persisted location files decoded at startup.
2. Prefer the newest timestamp-named files when the bound is exceeded.
3. Preserve chronological display order for the retained locations.
4. Keep per-file size, regular-file, coordinate, and JSON validation intact.

## Implementation Units

### Storage Load Boundary

File: `Journal/LocationsStorage.swift`

Introduce a visible maximum retained file count. Validate timestamp filenames
and file metadata before sorting candidates newest-first and taking the bound,
then decode and restore chronological order.

### Static Regression Contract

File: `scripts/check-baseline.py`

Require the count constant, timestamp parsing, newest-first selection, bounded
prefix, and existing per-file validation.

### Documentation

Files:

- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-bounded-location-file-count.md`

Document that the bound limits startup parsing rather than total files stored
on disk.

## Verification

- `python3 -m py_compile scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- hostile mutations removing the count bound or newest-first ordering
- `git diff --check`
- hosted push and pull-request project validation

## Boundaries

- Do not delete older files from disk in this change.
- Do not weaken the 64 KiB per-file limit or coordinate/JSON checks.
- Do not claim the bound limits directory enumeration itself.
