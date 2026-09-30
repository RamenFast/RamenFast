#!/usr/bin/env python3
"""Write RAMENFAST as stereo audio for an XY oscilloscope.

Left channel moves the beam across, right channel moves it up.
Play the output through Phosphor (or any XY scope) and the name appears.

Inside a glyph the beam only retraces strokes it already drew, fast,
so those returns hide under the lit line. Between glyphs the beam jumps
in a single sample, too fast to glow. The trace runs forward, then
back, so there is no long return trip at all.

usage: wordmark.py OUT.wav [--rate 48000] [--seconds 2] [--hz 60]
       wordmark.py OUT.wav --write-on 2.5 --hold 3   (beam writes the name, then holds)
"""
import argparse
import math
import struct
import wave

FAST = 8.0  # step multiplier for retraces over lit strokes
JUMP = 1e9  # pen-up: one sample


def arc(cx, cy, r, a0, a1, n=28):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), 1.0)
            for i in range(1, n + 1)]


def p(x, y, speed=1.0):
    return (x, y, speed)


def f(x, y):
    return (x, y, FAST)


# Each glyph: (advance width, [points]). A point's speed applies to the
# segment that arrives at it.
GLYPHS = {
    "R": (0.62, [p(0, 0), p(0, 1), p(0.34, 1)] + arc(0.34, 0.75, 0.25, 90, -90)
          + [p(0, 0.5), p(0.62, 0)]),
    "A": (0.68, [p(0, 0), p(0.34, 1), p(0.544, 0.4), p(0.136, 0.4),
                 f(0.544, 0.4), p(0.68, 0)]),
    "M": (0.76, [p(0, 0), p(0, 1), p(0.38, 0.32), p(0.76, 1), p(0.76, 0)]),
    "E": (0.54, [p(0, 0), p(0, 1), p(0.54, 1), f(0, 1), f(0, 0.5), p(0.44, 0.5),
                 f(0, 0.5), f(0, 0), p(0.54, 0)]),
    "N": (0.62, [p(0, 0), p(0, 1), p(0.62, 0), p(0.62, 1), f(0.62, 0)]),
    "F": (0.54, [p(0, 0), p(0, 1), p(0.54, 1), f(0, 1), f(0, 0.5), p(0.44, 0.5),
                 f(0, 0.5), f(0, 0)]),
    # S enters at the bottom of its lower bowl on the baseline, draws the
    # tail, sweeps up to the upper terminal, then retraces home fast.
    "S": (0.58, [p(0.29, 0)] + arc(0.29, 0.26, 0.26, -90, -150, 8)
          + arc(0.29, 0.26, 0.26, -150, 90) + arc(0.29, 0.75, 0.24, 270, 30)
          + [(x, y, FAST) for x, y, _ in arc(0.29, 0.75, 0.24, 30, 270)]
          + [(x, y, FAST) for x, y, _ in arc(0.29, 0.26, 0.26, 90, -90)]),
    # T rises from the baseline, draws its bar, retraces home.
    "T": (0.62, [p(0.31, 0), p(0.31, 1), p(0, 1), p(0.62, 1), f(0.31, 1), f(0.31, 0)]),
}

WORD = "RAMENFAST"
GAP = 0.24


def word_path():
    pts, x = [], 0.0
    for ch in WORD:
        width, glyph = GLYPHS[ch]
        for i, (px, py, sp) in enumerate(glyph):
            pts.append((x + px, py, JUMP if i == 0 else sp))
        x += width + GAP
    return pts, x - GAP


def resample(pts, step):
    out = [pts[0][:2]]
    for (x0, y0, _), (x1, y1, sp) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, round(d / (step * sp)))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(1, n + 1)]
    return out


def weighted_length(pts):
    return sum(math.hypot(x1 - x0, y1 - y0) / sp
               for (x0, y0, _), (x1, y1, sp) in zip(pts, pts[1:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--rate", type=int, default=48000)
    ap.add_argument("--seconds", type=float, default=2.0)
    ap.add_argument("--hz", type=float, default=60.0)
    ap.add_argument("--span", type=float, default=0.96, help="half width in scope units")
    ap.add_argument("--write-on", type=float, default=0.0,
                    help="seconds for the beam to write the name before holding")
    ap.add_argument("--hold", type=float, default=0.0)
    a = ap.parse_args()

    pts, total = word_path()
    # Ping-pong: forward then the same path backward.
    back = [(x, y, pts[i + 1][2]) for i, (x, y, _) in reversed(list(enumerate(pts[:-1])))]
    pts = pts + back
    per_frame = int(a.rate / a.hz)
    step = weighted_length(pts) / per_frame
    scale = 2 * a.span / total
    trace = [((x - total / 2) * scale, (y - 0.5) * scale) for x, y in resample(pts, step)]

    samples = []
    if a.write_on > 0:
        # Each frame draws a growing prefix of the trace, so the name writes itself.
        frames = int(a.write_on * a.hz)
        for k in range(1, frames + 1):
            t = k / frames
            t = 1 - (1 - t) ** 2  # ease out
            prefix = trace[:max(2, int(len(trace) * t))]
            reps = max(1, per_frame // len(prefix))
            for _ in range(reps):
                samples += prefix
        n_hold = int(a.rate * a.hold)
        samples += [trace[i % len(trace)] for i in range(n_hold)]
    else:
        n = int(a.rate * a.seconds)
        samples = [trace[i % len(trace)] for i in range(n)]

    with wave.open(a.out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(a.rate)
        w.writeframes(b"".join(struct.pack("<hh", int(x * 32000), int(y * 32000))
                               for x, y in samples))
    print(f"{a.out}: {len(trace)} samples per trace, {a.rate / len(trace):.1f} traces/s, "
          f"{len(samples) / a.rate:.2f} s, cap height {scale:.3f} scope units")


if __name__ == "__main__":
    main()
