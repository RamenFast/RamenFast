# The GitHub Field Guide

```text
╔═══════════════════════════════
║ ⚔️  ROOM  The Field Guide
║ 📍  Library
║ 🎨  #8B00FF violet
╚═══════════════════════════════
```

Mercer speaking. A front door should help someone choose a room. It should not ask a badge service whether the house exists.

## Pins: six doors, not six trophies

GitHub lets a profile show up to six pinned repositories and gists combined. Choose the rooms that best explain the work, not only the largest star counts.

Ben's own set, in his order, as of 2026-09-30: Phosphor, Holographic Eye, Phosphor Mobile, Bonsai 27B, the Phosphor Mobile dev line and SysMon. He gave the dev line its own pin on purpose, as the door for contributors. The README features these six in the same order, with a reason for each.

When the pins change, update the README to match. `art/build.sh` rebuilds the plates.

1. Open the profile's **Customize your pins** control.
2. Choose up to six public doors.
3. Order them from most approachable to most contextual.
4. Check the descriptions and preview on a phone.

Pins are Ben's choice. Agents feature them and never change them.

## README: help a stranger start

The public `RamenFast/RamenFast` repository's root `README.md` is the profile surface. Keep a clear name, one purpose, a few project doors and a reason to return.

- Keep terminal-art fences at 38 columns or fewer. Prose should wrap naturally.
- Use short lists instead of wide comparison tables.
- Store the banner in the repository and give it meaningful alt text.
- Link the living SymbolOS home first. Name the archive as the photograph.
- Describe what a project does without claiming its service is running.
- Check relative assets on the actual profile after pushing. The repository view alone is not the whole acceptance check.
- Date every statistic. A manual count is better than a badge that quietly fails.

## Releases: shipped work, not activity theater

A release should point at a real tag and verified artifacts. A documentation change does not need an app release.

1. Name the supported platform and install path.
2. Record the tested build and end-user check.
3. Attach checksums and clear release notes when shipping binaries.
4. Separate stable and prerelease lines.
5. Keep tags immutable after people depend on them.

Do not create empty releases to make a project look alive. No releases were created tonight.

## Social previews: one readable sign

A repository social preview is separate from the profile banner. GitHub's recommended image is 1280 × 640 pixels. Keep important content away from edges and readable when reduced.

Use the project's own instrument or geometry, a short name and one purpose. Do not put tiny CLI output or a wall of badges in it. A social preview is not proof of runtime state.

Set it in the repository's **Settings**, under **Social preview**, when that change is explicitly approved. This task did not upload previews or change settings.

## Contribution graph: a record with rules

GitHub decides what qualifies for the graph. Commits generally need an email associated with the account and must land on the default or `gh-pages` branch. Fork-only commits do not count like commits in a standalone repo. Other contributions include qualifying issues, pull requests and reviews.

Private contribution visibility is an account choice. Displaying private counts does not reveal private repository names. Different queries, calendars and visibility choices can produce different totals.

A graph is not hours worked, a quality score or a promise to work every day. Do not backdate commits, generate empty activity or claim private counts as public work. Preserve honest author dates and source history.

## No fake stats

The current [stats receipt](STATS-2026-09-30.md) gives the observed date, query scope and returned calendar. It counts owned public non-fork repositories, not all repositories visible to an authenticated account.

- Stars are summed across that exact repo set.
- Contributions are GitHub's returned total, not raw commit count.
- Language bytes are not skill or time spent. This profile omits language percentages.
- Do not add followers or stars from memory.
- If a query fails, keep the last dated receipt and label it stale.
- Do not expose access tokens in examples, workflows, screenshots or receipts.

The interrupted stats script is preserved as a [disabled draft](drafts/stats.py). It is not scheduled, linked as a runnable tool or part of the profile's maintenance contract. Its 100-repository and ten-language limits, unsafe width assumptions and missing API-error handling are reasons not to ship it as automation.

## Before the next publication

1. Inspect remote versus local history.
2. Check owned files and links.
3. Inspect code-fence widths and image alt text.
4. Confirm any statistics with a dated source.
5. Commit with a verification receipt.
6. Push normally, without rewriting shared history.
7. Check the published README and profile.

```text
        /\_/\
       ( o.o )  "Show the work.
        > ^ <    Not a fake score."
       /|   |\
      (_|   |_)  Rhy 🦊
```

🚪 EXITS

- → [Profile entrance](../README.md)
- → [GitHub profile README docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)
- → [Pinning docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/pinning-items-to-your-profile)
- → [Contribution rules](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions)
- → [Social preview docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- → [Release docs](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

💎 LOOT

- → A front door that can stand without a scoreboard.

☂🦊🐢
