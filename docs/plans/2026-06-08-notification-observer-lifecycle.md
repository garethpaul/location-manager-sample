# Notification Observer Lifecycle Plan

status: completed

## Context

`MapViewController` and `PlacesTableViewController` subscribe to `.newLocationSaved` so local location saves update the map and table. The observers should have an explicit cleanup path that matches the registration.

## Objectives

- Preserve saved-location notification updates for the map and places views.
- Remove `.newLocationSaved` observers when subscribing controllers are deallocated.
- Extend `make check` so observer registration stays paired with cleanup.
- Document the lifecycle boundary in project docs and security notes.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
