# Profile Publication Receipt: 2026-09-30

## Checked before publication

- `git fetch origin` showed local and remote main at `2e8ca16`, with a modified ASCII README and unfinished untracked stats script.
- Read both the remote-tracking README and local draft before editing. The remote page used external Vercel stats images. The final README has none.
- Preserved the banner, 1600 × 400 RGB PNG, and meaningful alt text. It stays repo-local.
- Rebuilt the profile around mobile-width terminal art, instruments, the living SymbolOS home and the frozen photograph.
- Profile README code fences measured at most **36 terminal display columns**. `station-tree lint` passed for README and the field guide.
- Public project doors returned HTTP 200. The guide's old contribution-doc URL returned 404, was replaced with its current official path and retested at HTTP 200.
- Authenticated GraphQL observation at about 09:11 UTC returned 18 owned public non-fork repos, eight summed stars, five followers and 2055 calendar contributions. [Scope and dates](STATS-2026-09-30.md).
- Kept the unverified language bars out. Dated counts are not live badges or productivity scores.
- Preserved the unfinished stats script under `docs/drafts/stats.py`. No workflow runs it. Ignored its Python bytecode cache instead of committing it.
- The README contains no cartograph reference. The stats receipt names the actual query set for honest accounting, not promotion.
- Wrote [the guide](GITHUB-GUIDE.md) for pins, README, releases, social previews, contribution graph rules and no fake stats.
- `git diff --check` passed. Prose lint found zero em dashes in README and the guide.

## Repeatable checks

From the profile repo root, using Ben's installed station checker:

```sh
station-tree lint README.md \
  docs/GITHUB-GUIDE.md --json

station-tree links README.md \
  docs/GITHUB-GUIDE.md \
  docs/STATS-2026-09-30.md \
  docs/ASKS.md \
  docs/VERIFICATION-2026-09-30.md \
  --json

git diff --check
```

The final content commit carries the local check receipt. Approved publication uses a standard push, never a force push. Remote equality and actual profile HTML are checked afterward and recorded in a closing receipt commit.

## Limits

No account settings, pins, social previews, repository visibility or releases were changed. This is guidance and a finished profile README, not a new stats service. No app was released or renamed.

No browser screenshot was taken. Phone-width acceptance uses fence-column and link checks. Rendering can vary by font. Saved statistics can go stale and should stay dated until a new observation replaces them.

[Profile](../README.md) · [Asks](ASKS.md) · [Field guide](GITHUB-GUIDE.md)
