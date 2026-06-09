# Changes

## 2026-06-09

- Added a saved-location JSON file filter before decoding persisted local
  documents.
- Added a places table index guard before reading saved locations during cell
  rendering.
- Added a redacted notification body for visit alerts so precise place
  descriptions stay inside the app.

## 2026-06-08

- Hardened local location persistence so document-directory, directory listing, JSON encoding, and file writes fail closed instead of force-unwrapping.
- Removed saved-location notification observers when map and places views are deallocated.
- Routed saved-location publishing through main-thread notification delivery before UIKit or MapKit observers update.
- Hardened location manager delegate setup so visit callbacks are wired before authorization and monitoring start.
- Switched saved location files to atomic `.json` writes while preserving existing decoded location history.
- Removed tracked Finder and Xcode user-state metadata.
- Added `.gitignore` rules and `make check` static baseline verification.
