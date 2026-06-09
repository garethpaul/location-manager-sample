# Places Table Index Guard Plan

status: completed

## Context

`PlacesTableViewController` renders rows from `LocationsStorage.shared`.
Saved-location notifications can reload the table while storage changes, so cell
rendering should not assume the row index is still valid after the row count was
computed.

## Objectives

- Snapshot saved locations before reading a row.
- Guard the row index before indexing into saved locations.
- Preserve existing cell reuse and location text rendering.
- Extend the static baseline and docs so the places table index guard remains
  visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
