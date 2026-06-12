# AGENTS.md

## Repository purpose

`garethpaul/location-manager-sample` is an Apple platform application or Objective-C/Swift sample. Journal Locations

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `Journal.xcodeproj` - Xcode project
- `Journal` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Local Apple development: `open Journal.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix: Swift 4.2, Python 3, GitHub Actions YAML, and Markdown.
- Preserve the iOS 12 deployment target, Swift 4.2 project settings, and unsigned project-parsing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `docs/plans/2026-06-09-latest-location-update-selection.md`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- Saved locations are local app documents data. Do not commit private GPX traces, exported location history, local `.xcconfig` files, or device-specific Xcode user state.
- Location persistence should remain local-only unless a future change includes explicit privacy design, retention notes, and security review.
- `LocationsStorage` should not force-unwrap document-directory, JSON, or file-write operations because location history is privacy-sensitive and should fail closed on storage errors.
- `LocationsStorage` should keep the saved-location JSON file filter before decoding files from local app documents.
- Keep regular-file, 64 KiB size, and valid-coordinate checks ahead of publishing decoded saved locations.
- Notification observer cleanup should stay paired with saved-location observer registration in map and places views.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
