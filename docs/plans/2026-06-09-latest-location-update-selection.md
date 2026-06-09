# Latest Location Update Selection

status: completed

## Context

The fake visit simulation path uses CoreLocation update batches to create a
sample visit. It previously read the first location in the batch, which can be
older than the most recent update.

## Completed Scope

- Switched fake visit simulation to use `locations.last`.
- Extended the static baseline to reject `locations.first` in that path.
- Updated README, VISION, SECURITY, and CHANGES to document latest location
  update selection.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
