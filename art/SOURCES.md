# Screenshot sources

Each file in [`shots/`](shots/) is a byte-for-byte copy of an image from a pinned repo, at the commit listed. Checked 2026-09-30 by comparing SHA-256 with the upstream raw file.

- `ph-inuse.png`: phosphor @ `70a3109`, `docs/inuse-full.png`
- `he-hero.png`: holographic-eye @ `4ca3b6f`, `docs/hero-blossom-dark.png`
- `pm-live.png`: phosphor-mobil3 @ `1f35f3c`, `docs/screenshots/kaleido-live.png`
- `pm-dense.png`: phosphor-mobil3 @ `1f35f3c`, `docs/screenshots/kaleido-dense.png`
- `pd-bestiary.png`: phosphor-mobil3-dev @ `a2f3924`, `docs/dev/receipts/bestiary-found.png`
- `pd-deck.png`: phosphor-mobil3-dev @ `a2f3924`, `docs/dev/receipts/art-inapp-deck.png`
- `sm-overview.png`: sysmon @ `cf5d728`, `docs/screenshot-overview.png`

The Holographic Eye screenshot uses synthetic demonstration data, as its own README states.

To recheck a file, fetch `https://raw.githubusercontent.com/RamenFast/REPO/COMMIT/PATH` and compare its `sha256sum` with the copy in `shots/`.
