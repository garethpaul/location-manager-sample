# Redacted Location Notification Body

status: completed

## Context

The app stores detailed reverse-geocoded place descriptions for saved visits and
shows them inside the table and map flows. Local notification alerts used the
same precise description as their body, which can expose location details
outside the app UI.

## Objectives

- Preserve detailed saved-location descriptions inside the app.
- Use a generic notification body for visit alerts.
- Keep notification title, sound, trigger, and saved-location publishing
  behavior unchanged.
- Extend the static baseline so precise place descriptions do not return to
  notification bodies.
- Document the privacy boundary beside local-only storage and notification
  delivery guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
