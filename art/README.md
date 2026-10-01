# Profile art

Every image on the [profile](../README.md) is built here, with one command:

```sh
art/build.sh
```

- `--check` verifies `assets/` against `ASSETS.sha256`.

Output lines are NDJSON events. Errors print a JSON object with a `fix`. Exit codes are 0 ok, 2 missing tool, 4 build failure.

## How it works

1. [`scope/wordmark.py`](scope/wordmark.py) writes `RAMENFAST` as stereo audio. The left channel moves the beam across and the right channel moves it up. Inside a letter the beam only retraces lines it already lit. Between letters it jumps in one sample, too fast to glow.
2. [`scope/lissajous.py`](scope/lissajous.py) writes one Lissajous figure per pin. Pin *n* is the ratio *n*:*n*+1, at the phase halfway between two retraced shapes, so each figure is as open as it can be.
3. The installed [Phosphor](https://github.com/RamenFast/phosphor) renders each file offline with `phosphor render --dump-frame`. It reads a scratch settings file under the build cache. Your own `~/.config/phosphor` is never read or written.
4. [`plates/plates.py`](plates/plates.py) lays out the hero and six plates as HTML, in pin order.
5. A private one-shot headless Thorium screenshots each plate. ImageMagick encodes them into `assets/`.

Play [`assets/ramenfast.wav`](../assets/ramenfast.wav) through any XY oscilloscope and the name appears.

## Needs

Python 3, Phosphor 4.7 or later, Thorium or another Chromium (`BROWSER_BIN`), ImageMagick, and the Inter and JetBrains Mono fonts.

## Inputs

- Screenshots are the pinned repos' own images. [SOURCES.md](SOURCES.md) lists each one by repo, path and commit.
- Plate titles are the real repo names. Taglines are each repo's own words from its README or description.
- Plates carry no version numbers or dated readings, so they stay true as the projects move. Keep it that way.
