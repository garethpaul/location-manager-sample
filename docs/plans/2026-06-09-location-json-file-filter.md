# Saved-Location JSON File Filter

status: completed

## Context

`LocationsStorage` writes saved locations with explicit `.json` filenames, but
startup loading still attempted to read and decode every file in the app
documents directory except `.DS_Store`. Local location history is sensitive, so
the decode path should stay limited to the app's saved-location JSON files.

## Objectives

- Filter persisted location files to `.json` before reading and decoding.
- Preserve existing fail-closed behavior for unreadable or malformed JSON files.
- Extend the static baseline so the JSON file filter remains visible without
  Xcode.
- Document the guard in README, vision, security, and changelog surfaces.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
