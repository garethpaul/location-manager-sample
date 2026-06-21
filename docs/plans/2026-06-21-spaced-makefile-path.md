# Spaced Makefile Path

status: completed

## Problem

GNU Make list functions split `MAKEFILE_LIST` on whitespace, so the documented
absolute `make -f` workflow failed when the checkout path contained spaces.

## Change

1. Derive the root from the raw Makefile path with shell-safe quote handling
   and POSIX `printf`/`sed` normalization.
2. Preserve `override ROOT` and reject `MAKEFILES`, command-line or environment
   replacement of `MAKEFILE_LIST`, and command-line shell replacement before
   root derivation or target execution.
3. Execute the real recipes for every verification alias from an unrelated
   directory against a path containing spaces, brackets, and a literal
   apostrophe.
4. Define the enforceable Make boundary as the repository Makefile being the
   sole explicitly loaded Makefile. Arbitrary additional `-f` files are
   caller-supplied programs, so use direct Python when Make parsing or shell
   selection is not trusted.
5. Run the hosted direct Python baseline before the Make convenience check so
   committed global or target-specific `ROOT` overrides and replacement
   recipes fail the candidate-tree consistency check before Make executes.
   This ordering is defense in depth for accidental or partial drift, not
   independent authentication: a pull request controls both the workflow and
   checker executed by the ordinary `pull_request` job.
6. Keep fork execution read-only and credential-free. The provider-bound
   required check identifies GitHub Actions as the reporting app, but does not
   independently attest the candidate workflow or checker contents.

## Verification

- Root and external `make lint`, `make test`, `make build`, and `make check`
  gates passed.
- Hostile `ROOT` values could not redirect commands.
- Command-line and environment `MAKEFILE_LIST` attacks failed closed.
- `MAKEFILES` and command-line `SHELL` attacks failed before repository root
  derivation or recipe execution.
- Hosted ordering mutations failed before Make execution, while the documented
  trust model explicitly avoids treating candidate-controlled code as an
  independent approval boundary.
- Portable verification executes real recipes rather than relying on dry-run
  command rendering.
- Hosted-equivalent validation fails before Make execution when a committed
  duplicate global `ROOT`, target-specific `ROOT`, or replacement `check`
  recipe is appended.
- No location service, saved location file, GPX route, Xcode build, signing, or
  simulator flow was used by portable verification.
