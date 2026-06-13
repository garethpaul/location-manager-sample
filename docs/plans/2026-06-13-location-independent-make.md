# Location-Independent Location Journal Verification

status: completed

## Context

Absolute Makefile invocations resolve `scripts/check-baseline.py` relative to
the caller instead of the checkout, so every documented gate fails outside the
repository directory.

## Scope

1. Derive the checkout root from the loaded Makefile.
2. Invoke the static checker by an absolute repository path.
3. Add exact Makefile, completed-plan, external-run, and guidance contracts.
4. Preserve location persistence, privacy boundaries, project metadata,
   workflow policy, and existing stacked-branch artifacts unchanged.

## Verification Plan

- Run `make lint`, `make test`, `make build`, and `make check` from the checkout
  and through an absolute Makefile path from a temporary directory.
- Run checker compilation, plist/XML/JSON/project parsing, and diff checks.
- Reject root derivation, checker invocation, plan status, plan evidence, and
  documentation mutations independently.
- Inspect intended paths, secret patterns, conflict markers, generated
  artifacts, and Swift/project/workflow changes before commit.

## Risk And Rollback

This changes verification path resolution only. Rollback restores the relative
checker recipe and removes its plan and documentation contracts.

## Verification

- All four Make aliases passed in root and external-directory runs through an
  absolute Makefile path; local Linux validation truthfully reported that
  `xcodebuild` is unavailable after the static baseline passed.
- Python checker compilation, plist/XML/JSON/project parsing, and
  `git diff --check` passed.
- Verification rejected five isolated hostile mutations by their intended
  contracts: root derivation, checker invocation, plan status, plan evidence,
  and README guidance.
- The intended five-file diff passed secret-pattern, conflict-marker,
  generated-artifact, and Swift/project/workflow change audits.
