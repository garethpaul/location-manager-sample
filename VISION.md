## Location Manager Sample Vision

Location Manager Sample is a Swift journal-style app that stores visited
locations, reverse-geocodes them, and displays saved places in a table and map.

The repository is useful as a CoreLocation, MapKit, local persistence, and
notification sample with a bundled GPX route for testing.

The goal is to keep the location journal understandable while making local data
storage and privacy boundaries explicit.

The current focus is:

Priority:

- Preserve location capture, reverse geocoding, local storage, and map display
- Keep route fixture and security policy aligned with the sample
- Avoid uploading or logging user location history
- Preserve license comments and attribution in source files

Next priorities:

- Add README setup, location permission, and GPX simulation instructions
- Add tests or manual checks for saving and displaying locations
- Modernize Swift/project settings in a dedicated pass
- Clarify retention and deletion behavior for saved locations

Contribution rules:

- One PR = one focused location, storage, map, or documentation change.
- Verify behavior with a simulator route or physical device when changing
  location logic.
- Keep generated signing files and private route data out of git.
- Document any change that transmits or stores location data differently.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)


Location history is sensitive. The app should remain local-first, avoid logging
precise locations, and make any retention, export, or sync behavior explicit.

## What We Will Not Merge (For Now)

- Background location upload or sync without privacy design
- Private route traces or location histories
- Broad project migration mixed with storage behavior changes
- Attribution/license removals

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
