# Hosted Project Validation

status: completed

## Context

The repository has focused static checks for local location persistence,
notification privacy, observer lifecycle, location delegate setup, project
wiring, and UI index safety, but no hosted validation. The checker also does not
parse the Xcode project when Xcode is available.

## Priorities

1. Add pinned, read-only, bounded macOS CI for the canonical `make check` gate.
2. Parse `Journal.xcodeproj` whenever Xcode is available.
3. Enforce the workflow contract from `scripts/check-baseline.py`.
4. Keep location access, saved location data, GPX playback, signing, simulator
   execution, and UI interaction outside hosted validation.

## Implementation Units

### Workflow And Checker

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`

Add push, pull-request, and manual triggers; read-only permissions; concurrency
cancellation; a bounded `macos-15` job; commit-pinned, credential-free checkout;
and `make check`. Require those properties structurally and run
`xcodebuild -list -project Journal.xcodeproj` when Xcode exists.

### Documentation

Files:

- `README.md`
- `VISION.md`
- `SECURITY.md`
- `CHANGES.md`
- `docs/plans/2026-06-10-hosted-project-validation.md`

Document project parsing as structural validation only, not location,
persistence, route, simulator, or UI-test coverage.

## Verification

- `python3 -m py_compile scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted macOS `Check` workflow for the pushed commit

## Boundaries

- Do not request location or inspect saved location files in CI.
- Do not introduce signing material or claim full legacy Swift build support.
