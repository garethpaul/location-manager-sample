# Location Manager Sample CI Baseline

## Status: Completed

## Context

`location-manager-sample` has a Python-backed static location, project, asset,
and privacy baseline behind `make check`. The repository needs that baseline to
run in GitHub Actions so location-storage and documentation guardrails are
checked before review.

## Objectives

- Run the existing `make check` wrapper in GitHub Actions.
- Keep the hosted job independent of simulator, signing, route playback, saved
  location data, and location services.
- Make the workflow presence part of the static baseline contract.

## Work Completed

- Added `.github/workflows/check.yml` to run `make check` on a bounded macOS 15
  job for pushes, pull requests, and manual dispatches.
- Added pinned, credential-free checkout, read-only permissions, and concurrency
  cancellation.
- Added `xcodebuild -list` project parsing when Xcode is available without
  building, signing, launching a simulator, or accessing location data.
- Extended `scripts/check-baseline.py` to require the CI workflow and this
  completed plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`

## Follow-Up Candidates

- Add a simulator route smoke job only after the supported Xcode, privacy, and
  route-test boundaries are documented.
