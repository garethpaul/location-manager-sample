# Changes

## 2026-06-26 10:53 PDT - P1 - Preserve rapid visit notifications

### Summary
Made each local visit notification request identifier unique so multiple saves
within the same formatted second cannot replace an earlier pending alert.

### Work completed
- Replaced the localized `dateString` identifier with a timestamp-plus-UUID value.
- Added a source-order contract, hostile regression, maintainer guidance, and a completed design record.

### Threads
- None; work completed directly to avoid overlap with active repositories.

### Files changed
- `Journal/AppDelegate.swift` — assigns unique identifiers before scheduling alerts.
- `scripts/check-baseline.py` — enforces identifier uniqueness and synchronized evidence.
- `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, `docs/plans/2026-06-26-unique-location-notification-identifiers.md` — document the boundary and cycle.

### Validation
- Focused baseline — passed after first failing on the old identifier.
- Isolated `dateString` mutation — rejected with the intended contract failure.
- `make lint`, `make test`, `make build`, `make check`, external absolute-Makefile verification, Python compilation, and whitespace audit — passed.
- Apple UserNotifications documentation — confirms reused identifiers replace pending requests.

### Bugs / findings
- P1 correctness: two rapid saves could collapse into one pending local notification.

### Blockers
- `xcodebuild` is unavailable on this Linux host; hosted macOS remains the project-parse boundary.

### Next action
- Publish the PR, verify hosted macOS and CodeQL gates, and merge only the green SHA.

## 2026-06-21

- Made absolute external Makefile invocations work when checkout paths contain
  spaces or a literal apostrophe while rejecting `ROOT` and `MAKEFILE_LIST`
  attempts to redirect verification.
- Made the sole-Makefile verification boundary explicit, rejected `MAKEFILES`
  and command-line shell replacement, and changed the portable oracle to run
  real recipes.
- Moved hosted validation to run the direct Python baseline before the Make
  convenience check, then parse the Xcode project, while documenting that the
  candidate-controlled workflow is a consistency guard rather than independent
  authentication.

## 2026-06-17

- Aligned successful-save pruning with the startup 64 KiB file-size boundary so
  oversized location-shaped JSON files do not displace valid retained entries.
- Bounded startup file reads before decode so a file replaced after metadata
  inspection cannot force an unbounded location JSON load.
- Rejected newly encoded location records over 64 KiB before file creation,
  pruning, or publication.

## 2026-06-16

- Added best-effort successful-save pruning toward the 1,000 newest compatible
  location JSON files while leaving unrelated documents untouched.

## 2026-06-15

- Bounded startup reads to the 1,000 newest eligible location JSON files while
  supporting both legacy timestamp and current timestamp-UUID filenames.

## 2026-06-14

- Rejected invalid new location coordinates before file creation or publication.
- Kept successful in-memory location saves ordered by date before notifying
  table and map observers.

## 2026-06-13

- Made every Make verification alias resolve the static checker from the
  checkout, including absolute Makefile invocations elsewhere.
- Added timestamp-prefixed unique JSON filenames for new location writes so
  equal timestamps cannot overwrite an earlier persisted record.

## 2026-06-12

- Stopped the hosted checkout from persisting its credential and added an exact
  static contract for the sole workflow and checkout step.

## 2026-06-10

- Bounded saved-location loading to regular JSON files up to 64 KiB and
  rejected decoded locations with invalid coordinates.
- Added pinned, read-only macOS hosted validation for `make check` and
  `Journal.xcodeproj` parsing without location or saved-data access.
- Added reverse-geocode fallback descriptions so local location saves still
  complete when the geocoder returns no placemark.

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static location manager baseline.
- Added a saved-location JSON file filter before decoding persisted local
  documents.
- Added a places table index guard before reading saved locations during cell
  rendering.
- Added a redacted notification body for visit alerts so precise place
  descriptions stay inside the app.
- Used the latest location update when fake visit simulation receives a
  CoreLocation batch.

## 2026-06-08

- Hardened local location persistence so document-directory, directory listing, JSON encoding, and file writes fail closed instead of force-unwrapping.
- Removed saved-location notification observers when map and places views are deallocated.
- Routed saved-location publishing through main-thread notification delivery before UIKit or MapKit observers update.
- Hardened location manager delegate setup so visit callbacks are wired before authorization and monitoring start.
- Switched saved location files to atomic `.json` writes while preserving existing decoded location history.
- Removed tracked Finder and Xcode user-state metadata.
- Added `.gitignore` rules and `make check` static baseline verification.
