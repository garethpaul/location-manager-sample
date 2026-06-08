# Location Storage Baseline Plan

## Context

`location-manager-sample` is a Swift iOS sample that stores visited locations in
the app documents directory, displays them in a table, and adds map
annotations. The repository also included generated Finder and Xcode user-state
files that should not be part of the project baseline.

## Risks

- File-system or encoding failures could crash the app because location
  persistence used force unwraps.
- Location history is privacy-sensitive; generated local metadata and private
  route/user state should stay out of git.
- Non-macOS hosts need a static verification path because Xcode builds are not
  always available.

## Work Completed

- Replaced force-unwraps in `LocationsStorage` with guarded document-directory
  resolution, best-effort directory reads, safe JSON decoding, and atomic writes.
- Saved new location files with a `.json` extension while continuing to decode
  existing location files in the documents directory.
- Removed tracked `.DS_Store`, workspace `UserInterfaceState.xcuserstate`, and
  per-user scheme-management metadata.
- Added `.gitignore`, `Makefile`, and `scripts/check-baseline.py`.
- Updated README, vision, and security notes for local-only location storage and
  static verification.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
