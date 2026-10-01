#!/usr/bin/env bash
# Rebuild every image on the profile from source.
#
#   art/build.sh           rebuild everything
#   art/build.sh --check   verify committed assets match art/ASSETS.sha256
#
# Pipeline:
#   1. scope/*.py write stereo WAV files (left = x, right = y).
#   2. The installed Phosphor renders them offline with a scratch settings file.
#      Ben's live ~/.config/phosphor is never read or written.
#   3. plates/plates.py writes HTML plates around those renders and the
#      pinned repos' own screenshots (art/shots, pinned by commit in SOURCES.md).
#   4. A private one-shot headless Thorium screenshots each plate.
#   5. ImageMagick encodes the final assets into assets/.
#
# Needs: python3, phosphor >= 4.7, thorium-browser, ImageMagick, Inter, JetBrains Mono.
set -euo pipefail

art="$(cd "$(dirname "$0")" && pwd)"
repo="$(dirname "$art")"
work="${ART_WORK:-${XDG_CACHE_HOME:-$HOME/.cache}/ramenfast-profile-art}"
out="$repo/assets"
mkdir -p "$work/img" "$work/html" "$work/png" "$out"

emit() { printf '{"event":"%s","tool":"profile-art",%s}\n' "$1" "$2"; }
fail() { printf '{"status":"error","tool":"profile-art","error":"%s","fix":"%s"}\n' "$1" "$2" >&2; exit "${3:-4}"; }

command -v phosphor >/dev/null || fail "phosphor not on PATH" "install Phosphor 4.7+ from github.com/RamenFast/phosphor/releases" 2
command -v thorium-browser >/dev/null || fail "thorium-browser not on PATH" "install Thorium or set BROWSER_BIN to a Chromium" 2
command -v convert >/dev/null || fail "ImageMagick convert not on PATH" "apt install imagemagick" 2
browser="${BROWSER_BIN:-thorium-browser}"

if [[ "${1:-}" == "--check" ]]; then
  (cd "$repo" && sha256sum -c art/ASSETS.sha256) || fail "asset hashes differ" "run art/build.sh and commit assets/ with art/ASSETS.sha256" 4
  emit ok '"checked":"art/ASSETS.sha256"'
  exit 0
fi

# Render one WAV through Phosphor with a private settings file.
# usage: scope IN.wav OUT_BASENAME WxH FRAME SETTINGS_JSON
scope() {
  local home="$work/phosphor-home-$2"
  mkdir -p "$home/.config/phosphor"
  printf '%s' "$5" > "$home/.config/phosphor/settings.json"
  HOME="$home" PIPEWIRE_RUNTIME_DIR="/run/user/$(id -u)" \
    timeout 120 phosphor render "$1" "$work/$2.mp4" --size "$3" \
    --dump-frame "$4:$work/$2.ppm" --json >/dev/null 2>&1 \
    || fail "phosphor render failed for $2" "run: phosphor render $1 /tmp/x.mp4 --json and read its fix" 4
  convert "$work/$2.ppm" "$work/$2.png"
  emit scope "\"name\":\"$2\""
}

# Screenshot one HTML file with a private headless browser.
# Old headless loses 121 px of the window to chrome. Ask for extra, crop back.
# Headless writes the PNG, then lingers. Wait for the file, then stop it.
shot() {
  local raw="$2.raw.png"
  rm -f "$2" "$raw"
  timeout 90 "$browser" --headless --disable-gpu --no-first-run --disable-sync \
    --disable-extensions --disable-background-networking --disable-component-update \
    --user-data-dir="$work/browser-$(basename "$2" .png)" --hide-scrollbars \
    --force-device-scale-factor=1 --virtual-time-budget=4000 \
    --window-size="$3,$(($4 + 121))" --screenshot="$raw" \
    "file://$1" >/dev/null 2>&1 &
  local pid=$! size=0 last=-1
  for _ in $(seq 1 180); do
    sleep 0.5
    size=$(stat -c %s "$raw" 2>/dev/null || echo 0)
    if [[ "$size" -gt 0 && "$size" == "$last" ]]; then break; fi
    last=$size
    kill -0 "$pid" 2>/dev/null || break
  done
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  [[ -s "$raw" ]] || fail "no screenshot for $1" "open $1 in a browser to check it loads, then rerun" 4
  convert "$raw" -crop "${3}x${4}+0+0" +repage "$2"
  rm -f "$raw"
}

# 1-2. Wordmark: RAMENFAST drawn by the beam, P7 green on a graticule.
python3 "$art/scope/wordmark.py" "$work/wordmark.wav" --rate 96000 --span 0.8 --seconds 3 >/dev/null
scope "$work/wordmark.wav" wordmark 1600x1600 150 \
  '{"display_mode":"xy","theme_name":"P7 Green","gain":1.0,"auto_gain":false,"beam_energy":5,"beam_focus":0.9,"persistence":0.3,"grid_enabled":true,"amoled_background":true,"kit_enabled":false,"beam_cycle_count":1,"scope_sample_rate":96000}'
convert "$work/wordmark.png" -gravity center -crop 1600x500+0+0 +repage "$work/img/hero-band.png"

# Six pin signatures: Lissajous n:(n+1), one tube colour per pin.
colours=("0.42,1.0,0.55" "0.91,0.54,0.65" "0.35,0.75,1.0" "1.0,0.62,0.12" "1.0,0.30,0.30" "0.20,1.0,0.92")
for i in 1 2 3 4 5 6; do
  python3 "$art/scope/lissajous.py" "$work/sig$i.wav" "$i" >/dev/null
  scope "$work/sig$i.wav" "sig$i" 720x720 120 \
    "{\"display_mode\":\"xy\",\"theme_name\":\"Custom\",\"custom_beam_color\":[${colours[$((i-1))]}],\"beam_cycle_count\":1,\"gain\":1.0,\"auto_gain\":false,\"beam_energy\":5,\"beam_focus\":0.9,\"persistence\":0.3,\"grid_enabled\":false,\"amoled_background\":true,\"kit_enabled\":false,\"scope_sample_rate\":96000}"
  convert "$work/sig$i.png" -crop 600x600+60+60 +repage -resize 300x300 "$work/img/sig$i.png"
done

# 3. Plates.
cp "$art"/shots/*.png "$work/img/"
rm -f "$work"/html/*.html "$work"/png/*.png
ART_WORK="$work" python3 "$art/plates/plates.py" >/dev/null

# 4. Screenshots, in parallel.
pids=()
for f in "$work"/html/*.html; do
  b="$(basename "$f" .html)"; h=500; [[ "$b" == 00-hero ]] && h=640
  shot "$f" "$work/png/$b.png" 1600 "$h" &
  pids+=("$!")
done
for pid in "${pids[@]}"; do
  wait "$pid" || fail "a plate screenshot failed" "rerun art/build.sh and read the error line above" 4
done

# 5. Encode. Plates are photographic: high-quality JPEG keeps the page light.
rm -f "$out"/0[0-6]-*.jpg
for f in "$work"/png/*.png; do
  b="$(basename "$f" .png)"
  convert "$f" -strip -sampling-factor 4:4:4 -quality 90 "$out/$b.jpg"
  emit asset "\"file\":\"assets/$b.jpg\",\"bytes\":$(stat -c %s "$out/$b.jpg")"
done
# The playable wordmark: small enough to download, loud enough to see.
python3 "$art/scope/wordmark.py" "$out/ramenfast.wav" --rate 48000 --seconds 2 >/dev/null

(cd "$repo" && sha256sum assets/*.jpg > art/ASSETS.sha256)
printf '{"status":"ok","tool":"profile-art","assets":"%s","work":"%s"}\n' "$out" "$work"
