# Location Notification Main-Thread Plan

status: completed

## Context

`LocationsStorage` posts `.newLocationSaved` after writing a local location
file. The map and places views observe that notification and update UIKit or
MapKit state, so saved-location delivery should happen on the main thread even
if a future save path runs from a background callback.

## Objectives

- Preserve atomic local JSON writes before publishing a saved location.
- Append saved locations and post `.newLocationSaved` from one helper.
- Dispatch saved-location publishing to the main queue when the save path is not
  already on the main thread.
- Extend `make check` so future storage changes preserve main-thread
  notification delivery.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
