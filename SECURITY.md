# Security Policy

## Supported Versions

The supported security scope for `location-manager-sample` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: Journal Locations

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/location-manager-sample` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be an Apple platform application or Swift sample. The active security scope is the code and documentation on the default branch.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found mobile permission or privacy-sensitive data handling; changes in those areas should receive security-focused review before merge.
- Review found file, document, data, or media parsing flows; changes in those areas should receive security-focused review before merge.
- `make check` runs `scripts/check-baseline.py` to verify local location-storage guardrails, generated-file ignores, project metadata, assets, plists, storyboards, and privacy documentation.
- The pinned macOS workflow only parses project metadata and static resources;
  it does not request location, inspect saved location JSON, play the GPX route,
  build or sign the app, launch a simulator, or exercise UI flows.
- Saved location history should remain local app documents data. Changes that export, upload, sync, log, or broaden retention of locations need explicit privacy review.
- Saved-location JSON file filter handling should stay before decoding local app documents so unrelated files are ignored.
- Saved-location loading should accept only regular JSON files up to 64 KiB and
  reject invalid coordinates before decoded data reaches the UI.
- Location manager delegate setup should happen before authorization and visit monitoring so visit callbacks are handled by the app delegate.
- Fake visit simulation should use the latest location update from CoreLocation
  batches instead of an older sample.
- Views that observe saved-location notifications should remove those notification observers when deallocated.
- Saved-location publishing should keep main-thread notification delivery because notification observers update UIKit and MapKit state.
- Local visit notifications should use a redacted notification body rather than exposing precise place descriptions outside the app.
- Reverse-geocode fallback descriptions should keep local location saves
  available without requiring a precise placemark.
- The places table index guard should remain before reading saved locations because notification-driven updates can change storage between row counting and cell rendering.
- Generated Finder metadata, Xcode `xcuserdata`, `.xcuserstate`, local `.xcconfig`, private GPX traces, and exported location histories must stay out of git.
- No primary dependency manifest was detected in the repository root. If dependencies are added later, include a manifest and prefer reproducible installation instructions.

## Mobile Privacy Notes

If this project requests device permissions such as location, camera, microphone, contacts, Bluetooth, health data, or local storage access, reports should describe the permission involved and whether sensitive data can be accessed, persisted, or transmitted unexpectedly. Please avoid testing against real third-party user data or accounts you do not control.

For this sample, reports should also state whether the issue affects always-on
visit monitoring, local JSON location files, notifications, map annotations, or
the bundled `Route.gpx` test fixture. Storage errors and notification observer
lifecycle issues should fail closed without crashing the app or printing precise
location history.
Saved-location main-thread notification delivery should remain in place before
UIKit or MapKit observers update. The redacted notification body should keep
precise place descriptions inside the app UI rather than lock-screen alerts.
Reverse-geocode fallback descriptions should keep local saves available when
geocoding cannot resolve a placemark.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
