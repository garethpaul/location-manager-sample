# Checkout Credential Boundary

status: completed

## Context

The recorded remediation evidence describes the hosted checkout as
credential-free, but the exact workflow head still uses the checkout action's
default credential persistence. The macOS validation job only needs repository
contents to run the offline baseline and parse the Xcode project.

## Objectives

- Disable checkout credential persistence without changing hosted coverage.
- Make the checker reject missing, duplicate, relocated, or contradictory
  checkout boundary declarations.
- Keep the pinned action, read-only permissions, macOS runner, timeout,
  concurrency policy, and `make check` command unchanged.
- Correct repository documentation so it matches the exact workflow state.

## Implementation Units

### Workflow And Static Contract

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`

Add the non-persisted credential option under the sole pinned checkout step.
Require exactly one workflow file, checkout action, checkout options block, and
`persist-credentials: false` declaration. Reject write permissions and any
contradictory credential setting while preserving the existing hosted project
parse contract.

### Documentation

Files:

- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-checkout-credential-boundary.md`

Record the narrower workflow credential lifetime and the completed local
verification. Keep structural hosted validation distinct from device, route,
location authorization, persistence, simulator, and UI coverage.

## Work Completed

- Added `persist-credentials: false` beneath the sole pinned checkout step.
- Added exact workflow-file, checkout-action, options-block, and credential
  declaration counts to `scripts/check-baseline.py`.
- Rejected duplicate permission blocks, write scopes, and contradictory
  persisted-credential settings while preserving the existing least-privilege
  workflow contract.
- Updated README, security, vision, and changelog documentation.

## Verification Completed

- `python3 -m py_compile scripts/check-baseline.py`
- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- Hostile mutations for removed, duplicated, relocated, contradictory, and
  unpinned checkout configuration

Local verification reports `xcodebuild` unavailable on Linux and therefore
proves the dependency-free static baseline only. Canonical hosted macOS checks
remain required at the exact successor head before owner merge.

## Boundaries

- Do not change Swift source, Xcode project files, GPX data, or persistence.
- Do not request location access, inspect saved locations, add signing, or claim
  device/runtime coverage.
- Do not alter the existing remediation PR or its protected evidence.
