# Reverse-Geocode Fallback Description

status: completed

## Context

Visit and map-added location saves depended on reverse geocoding returning a
placemark description. If the geocoder returned no placemark, the app could skip
saving an otherwise valid local coordinate.

## Completed Scope

- Saved visit locations with a generic fallback description when reverse
  geocoding has no placemark.
- Preserved fake-visit and map-added location save flows.
- Kept precise place descriptions inside the app when a placemark is available.
- Extended the static baseline and docs so reverse-geocode fallback descriptions
  remain explicit.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
