#!/usr/bin/env python3
"""Lissajous signature for pin N: x = sin(N t + phase), y = sin((N+1) t).

usage: lissajous.py OUT.wav N [--rate 96000] [--seconds 3]
"""
import argparse
import math
import struct
import wave

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("n", type=int)
ap.add_argument("--rate", type=int, default=96000)
ap.add_argument("--seconds", type=float, default=3.0)
ap.add_argument("--base", type=float, default=60.0, help="Hz of one full figure")
a = ap.parse_args()

n = a.n
# Retraced (degenerate) phases sit pi/b apart. Take the midpoint between two.
b = n + 1
phase = math.pi / 2 - (n - 1) * math.pi / (2 * b)
with wave.open(a.out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(a.rate)
    frames = bytearray()
    for i in range(int(a.rate * a.seconds)):
        t = 2 * math.pi * a.base * i / a.rate
        x = math.sin(n * t + phase)
        y = math.sin(b * t)
        frames += struct.pack("<hh", int(x * 0.8 * 32000), int(y * 0.8 * 32000))
    w.writeframes(bytes(frames))
print(f"{a.out}: pin {n} -> {n}:{n + 1}")
