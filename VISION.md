## Location Manager Sample Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Location Manager Sample is a Swift journal-style app that stores visited
locations, reverse-geocodes them, and displays saved places in a table and map.

The repository is useful as a CoreLocation, MapKit, local persistence, and
notification sample with a bundled GPX route for testing.

The goal is to keep the location journal understandable while making local data
storage and privacy boundaries explicit.

Current baseline: `make lint`, `make test`, `make build`, and `make check` run
`scripts/check-baseline.py` to verify project files, route fixtures,
plist/storyboard/assets, local location-storage guardrails, main-thread notification
delivery, generated metadata ignores, and privacy documentation.

The current focus is:

Priority:

- Preserve location capture, reverse geocoding, local storage, and map display
- Keep route fixture and security policy aligned with the sample
- Keep location storage local-only and resilient to file-system/JSON failures
- Keep saved-location JSON file filter handling before decoding local documents
- Keep saved-location loads limited to regular JSON files up to 64 KiB and
  reject decoded invalid coordinates
- New location writes use timestamp-prefixed unique JSON filenames so equal
  timestamps preserve separate local records
- Keep location manager delegate setup ahead of authorization and visit monitoring
- Keep fake visit simulation using the latest location update from CoreLocation batches
- Preserve reverse-geocode fallback descriptions when a placemark is unavailable
- Pair saved-location notification observer registration with cleanup
- Keep saved-location notification delivery on the main thread for UIKit/MapKit observers
- Keep precise place descriptions out of the redacted notification body
- Keep the places table index guard before reading saved locations
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep hosted project validation pinned, read-only, and credential-free on
  macOS through `Journal.xcodeproj` parsing and `make check`
- Keep generated Finder and Xcode user-state metadata out of git
- Avoid uploading or logging user location history
- Preserve license comments and attribution in source files

Next priorities:

- Add README setup, location permission, and GPX simulation instructions
- Add tests or manual checks for saving and displaying locations
- Modernize Swift/project settings in a dedicated pass
- Clarify retention and deletion behavior for saved locations

Contribution rules:

- One PR = one focused location, storage, map, or documentation change.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing
  Swift, project, route, asset, plist, storyboard, or documentation changes.
- Verify behavior with a simulator route or physical device when changing
  location logic.
- Keep generated signing files and private route data out of git.
- Document any change that transmits or stores location data differently.
- Preserve notification observer lifecycle cleanup when changing map or places views.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Location history is sensitive. The app should remain local-first, avoid logging
precise locations, and make any retention, export, or sync behavior explicit.
Storage failures should fail closed rather than crashing or exposing location
history in logs, and saved-location JSON file filter handling should keep
unrelated local documents out of the decode path. Regular-file, 64 KiB size,
and coordinate-validity checks should bound persisted input before it reaches
the UI. Saved-location notification observer cleanup and main-thread
notification delivery should remain explicit for views that subscribe to local
storage changes. The redacted notification body should avoid showing precise
place descriptions outside the app.

## What We Will Not Merge (For Now)

- Background location upload or sync without privacy design
- Private route traces or location histories
- Broad project migration mixed with storage behavior changes
- Attribution/license removals

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
