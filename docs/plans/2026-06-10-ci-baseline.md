# Location Manager Sample CI Baseline

## Status: Completed

## Context

`location-manager-sample` has a Python-backed static location, project, asset,
and privacy baseline behind `make check`. The repository needs that baseline to
run in GitHub Actions so location-storage and documentation guardrails are
checked before review.

## Objectives

- Run the existing `make check` wrapper in GitHub Actions.
- Keep the hosted job independent of Xcode, simulator, and location services.
- Make the workflow presence part of the static baseline contract.

## Work Completed

- Added `.github/workflows/check.yml` to run `make check` on pushes, pull
  requests, and manual dispatches.
- Set up Python 3.12 for the static checker.
- Extended `scripts/check-baseline.py` to require the CI workflow and this
  completed plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`

## Follow-Up Candidates

- Add a macOS/Xcode build or simulator route smoke job once the supported Xcode
  and route-test baseline are documented.
