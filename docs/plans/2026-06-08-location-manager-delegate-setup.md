# Location Manager Delegate Setup Plan

status: completed

## Context

The app delegate requested always-on location authorization and started visit monitoring before assigning itself as the `CLLocationManager` delegate. Assigning the delegate first keeps early authorization or visit callbacks routed to the sample's handler.

## Objectives

- Assign the location manager delegate before requesting authorization.
- Start visit monitoring only after the delegate is wired.
- Extend the static baseline and docs to keep location manager delegate setup order visible.

## Verification

- `make check`
- `git diff --check`
