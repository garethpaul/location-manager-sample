# Chronological Location Publishing

Status: completed

## Problem

Persisted locations are sorted by date during startup, but successful saves are
always appended to the in-memory collection. Reverse-geocode callbacks can
complete out of order, so the places list can lose chronological ordering until
the next launch even though the on-disk data is correct.

## Scope

- Keep `LocationsStorage.locations` ordered by `Location.date` after each
  successful save.
- Preserve atomic file writes, success-only publication, main-thread mutation,
  and saved-location notifications.
- Extend the maintained static baseline and documentation for the ordering
  contract.
- Do not change persistence formats, filename generation, geocoding, retention,
  map annotations, or notification content.

## Implementation

1. Update `Journal/LocationsStorage.swift` so the main-thread publication block
   inserts each saved location at its chronological position instead of always
   appending it.
2. Extend `scripts/check-baseline.py` with a mutation-sensitive contract for the
   sorted insertion and its placement before notification delivery.
3. Record the behavior and maintenance boundary in `README.md`, `VISION.md`,
   `SECURITY.md`, and `CHANGES.md`.

## Validation

- Run `python3 -m py_compile scripts/check-baseline.py`.
- Run `make lint`, `make test`, `make build`, and `make check` from the checkout
  and run the canonical check from an external directory.
- Verify isolated mutations that restore unconditional append, reverse the date
  comparison, move notification delivery before insertion, or leave this plan
  incomplete are rejected.
- Run `git diff --check` and explicit generated-artifact, secret-pattern, and
  intended-path audits.
- Record that Xcode and simulator execution are unavailable on this Linux host;
  rely on the existing macOS hosted baseline for exact-head compilation.

## Risks

- Equal timestamps need stable placement; inserting after existing equal-date
  entries preserves publication order.
- The stacked base PR must remain available and merge before this change.

## Verification Completed

- `python3 -m py_compile scripts/check-baseline.py` passed.
- All four Make gates passed from the checkout, and the canonical check passed
  from an external directory through the absolute Makefile path.
- Six isolated hostile mutations were rejected: unconditional append, reversed
  date comparison, notification-before-insertion ordering, removed end-index
  fallback, stale plan status, and missing maintenance guidance.
- `git diff --check` and explicit intended-path, generated-artifact, and
  secret-pattern audits passed.
- `xcodebuild` is unavailable on this Linux host, so no simulator, device, Core
  Location callback, or live filesystem runtime verification is claimed.
