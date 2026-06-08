# Changes

## 2026-06-08

- Hardened local location persistence so document-directory, directory listing, JSON encoding, and file writes fail closed instead of force-unwrapping.
- Removed saved-location notification observers when map and places views are deallocated.
- Switched saved location files to atomic `.json` writes while preserving existing decoded location history.
- Removed tracked Finder and Xcode user-state metadata.
- Added `.gitignore` rules and `make check` static baseline verification.
