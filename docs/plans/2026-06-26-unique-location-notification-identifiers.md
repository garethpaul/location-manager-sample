# Unique Location Notification Identifiers

status: completed

## Problem

`newVisitReceived` used the localized, second-resolution `location.dateString`
as the `UNNotificationRequest` identifier. Apple documents that a reused
notification request identifier replaces the pending request. Two rapid saves
that format to the same value could therefore persist as separate journal
entries while only the later alert remained pending.

## Alternatives Considered

- **Timestamp plus UUID (selected):** preserves rough event correlation while
  guaranteeing uniqueness without coordinates or mutable controller state.
- **UUID only:** equally unique but less inspectable during local debugging.
- **Process-local sequence number:** deterministic but introduces restoration
  and synchronization state that the sample does not otherwise need.

## Decision

- Build a notification identifier from `location.date.timeIntervalSince1970`
  and a fresh `UUID` before creating the request.
- Keep the redacted title/body, one-second trigger, persistence, geocoding, and
  notification authorization behavior unchanged.
- Enforce construction order and reject a return to `location.dateString` in the
  portable baseline.

## Verification Completed

- The new static assertion failed against the original `dateString` request.
- The focused baseline passed after the timestamp-UUID identifier was added.
- The isolated dateString mutation was rejected with the intended failure.
- All four Make aliases, external absolute-Makefile verification, Python
  compilation, and whitespace checks passed. xcodebuild was unavailable on the
  Linux host, so Xcode project parsing remains hosted macOS evidence.

## Scope Boundaries

This change does not alter notification contents, request timing, location
retention, reverse geocoding, authorization, or delivered-notification cleanup.

## External Evidence

- Apple `UNNotificationRequest.identifier` documentation:
  https://developer.apple.com/documentation/usernotifications/unnotificationrequest/identifier
