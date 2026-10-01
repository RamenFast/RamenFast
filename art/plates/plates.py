#!/usr/bin/env python3
"""Build the profile hero and six pin plates as HTML, in Ben's pin order.

Titles are the real repo names. Taglines are each repo's own words,
from its README or description. Keyword rows carry what the repo does.
Plates hold no version numbers or dated measurements, so they stay true
as the projects move. Screenshots are the repos' own, listed in
art/SOURCES.md.
usage: ART_WORK=DIR plates.py   (reads DIR/img, writes DIR/html/*.html)
"""
import json
import os
import pathlib

WORK = pathlib.Path(os.environ["ART_WORK"])
OUT = WORK / "html"
OUT.mkdir(exist_ok=True)

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:500px;overflow:hidden;background:#07080a}
body{font-family:Inter,sans-serif;color:#f1edf1;-webkit-font-smoothing:antialiased}
.plate{position:absolute;inset:0;background:var(--bg);overflow:hidden}
.grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),
                   linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:40px 40px;background-position:-1px -1px}
.glow{position:absolute;width:900px;height:900px;left:-300px;top:-420px;
  background:radial-gradient(circle,var(--halo) 0%,transparent 60%)}
.frame{position:absolute;inset:14px;border:1px solid var(--line)}
.tick{position:absolute;width:14px;height:14px;border-color:var(--accent);border-style:solid;opacity:.9}
.tl{left:14px;top:14px;border-width:2px 0 0 2px}.tr{right:14px;top:14px;border-width:2px 2px 0 0}
.bl{left:14px;bottom:14px;border-width:0 0 2px 2px}.br{right:14px;bottom:14px;border-width:0 2px 2px 0}
.text{position:absolute;left:64px;top:52px;width:680px;bottom:52px;display:flex;flex-direction:column}
.eyebrow{display:flex;align-items:center;gap:18px;font:600 21px/1 'JetBrains Mono',monospace;
  letter-spacing:.14em;color:var(--accent);text-transform:uppercase}
.eyebrow .sig{width:64px;height:64px;margin:-8px 0 -8px -6px}
.eyebrow .rule{flex:0 0 40px;height:1px;background:var(--accent);opacity:.6}
.eyebrow .stack{color:rgba(241,237,241,.55);letter-spacing:.1em}
h1{font:750 var(--title,86px)/1 Inter,sans-serif;letter-spacing:-.025em;margin-top:34px;white-space:nowrap}
.tag{font:400 31px/1.32 Inter,sans-serif;color:rgba(241,237,241,.78);margin-top:20px;max-width:660px}
.keys{margin-top:auto;padding-top:18px;border-top:1px solid var(--line);
  font:500 21px/1.5 'JetBrains Mono',monospace;letter-spacing:.03em;color:var(--accent)}
.keys i{font-style:normal;color:rgba(241,237,241,.35);padding:0 .45em}
.media{position:absolute;right:48px;top:44px;bottom:44px;left:800px;display:flex;gap:20px;
  justify-content:flex-end;align-items:stretch}
.shot{position:relative;border:1px solid var(--line-strong);background:#000;overflow:hidden;
  box-shadow:0 0 0 1px rgba(0,0,0,.6),0 30px 80px -30px var(--halo)}
.shot img{display:block;width:100%;height:100%;object-fit:cover}
.panel{border:1px solid var(--line-strong);background:rgba(0,0,0,.55);padding:30px 34px;
  font:500 22px/1.7 'JetBrains Mono',monospace;color:rgba(241,237,241,.82);align-self:center}
.panel .k{color:rgba(241,237,241,.45)}
.panel .a{color:var(--accent)}
"""


def theme(r, g, b):
    rgb = f"{r},{g},{b}"
    return (f"--accent:rgb({rgb});--grid:rgba({rgb},.055);--halo:rgba({rgb},.16);"
            f"--line:rgba({rgb},.22);--line-strong:rgba({rgb},.38);"
            f"--bg:rgb({round(4 + r * .018)},{round(5 + g * .018)},{round(7 + b * .018)})")


def plate(n, accent, stack, name, tag, keys, media, title=86):
    sig = f"../img/sig{n}.png"
    chips = "<i>·</i>".join(keys)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head>
<body><div class="plate" style="{theme(*accent)};--title:{title}px">
<div class="glow"></div><div class="grid"></div><div class="frame"></div>
<div class="tick tl"></div><div class="tick tr"></div><div class="tick bl"></div><div class="tick br"></div>
<div class="text">
  <div class="eyebrow"><img class="sig" src="{sig}"><span>Pin 0{n}</span><span class="rule"></span><span class="stack">{stack}</span></div>
  <h1>{name}</h1>
  <p class="tag">{tag}</p>
  <div class="keys">{chips}</div>
</div>
<div class="media">{media}</div>
</div></body></html>"""


def shot(src, width, pos="center"):
    return (f'<div class="shot" style="width:{width}px"><img src="../img/{src}" '
            f'style="object-position:{pos}"></div>')


# Titles: repo names. Taglines: the repo's own words (README or description).
PLATES = [
    dict(slug="01-phosphor", accent=(107, 255, 140), stack="Rust · wgpu · PipeWire",
         name="phosphor",
         tag="A GPU oscilloscope for everything your PC plays.",
         keys=["P7 beam", "mix apps", "drive Spotify", "agent CLI"],
         media=shot("ph-inuse.png", 720, "50% 30%")),
    dict(slug="02-holographic-eye", accent=(231, 138, 166), stack="Rust · Tauri · Zig/WASM",
         name="holographic-eye", title=76,
         tag="Glass cockpit for the Hermes holographic memory.",
         keys=["real HRR geometry", "journaled", "undoable", "themable"],
         media=shot("he-hero.png", 720, "30% 40%")),
    dict(slug="03-phosphor-mobil3", accent=(89, 191, 255), stack="Kotlin · Compose · Rust",
         name="phosphor-mobil3", title=78,
         tag="A CRT oscilloscope in your pocket.",
         keys=["120 Hz", "playback capture", "signed APK", "no tracking"],
         media=shot("pm-live.png", 290, "50% 50%") + shot("pm-dense.png", 290, "50% 50%")),
    dict(slug="04-bonsai27b-vulkan", accent=(255, 158, 31), stack="Vulkan · llama.cpp · RDNA2",
         name="bonsai27b-vulkan", title=74,
         tag="Ternary Bonsai-27B on a 12&nbsp;GB AMD card via Vulkan. No ROCm.",
         keys=["1.71 bpw", "262K context", "receipts"],
         media="""<div class="panel" style="width:700px">
<div><span class="a">$</span> ./install.sh</div>
<div class="k">  deps check → fork build →</div>
<div class="k">  model download → GPU smoke test</div>
<div style="margin-top:14px"><span class="a">$</span> ./run.sh</div>
<div class="k">  OpenAI-compatible API + web UI</div>
<div class="k">  → http://127.0.0.1:8080</div>
</div>"""),
    dict(slug="05-phosphor-mobil3-dev", accent=(255, 92, 92), stack="Kotlin · Rust · Tailscale",
         name="phosphor-mobil3-dev", title=66,
         tag="The experiment line. Features land here first, break here first, and get fixed here first.",
         keys=["PC relay", "geometry FX", "open Discussions"],
         media=shot("pd-bestiary.png", 290, "50% 22%") + shot("pd-deck.png", 290, "50% 78%")),
    dict(slug="06-sysmon", accent=(51, 255, 235), stack="Rust · egui · JSON API",
         name="sysmon",
         tag="A compact system monitor for AMD-GPU Linux desktops, and a system state API you can script against.",
         keys=["probe", "tap", "ctl", "schema"],
         media="""<div class="panel" style="width:430px;font-size:21px">
<div><span class="a">$</span> sysmon probe gpu</div>
<div><span class="a">$</span> sysmon tap network</div>
<div><span class="a">$</span> sysmon ctl &lt;verb&gt;</div>
<div><span class="a">$</span> sysmon schema</div>
<div class="k" style="margin-top:12px">one binary: window,</div>
<div class="k">engine, CLI, socket</div>
</div>""" + shot("sm-overview.png", 270, "50% 0%")),
]

for p in PLATES:
    slug = p.pop("slug")
    n = int(slug[:2])
    (OUT / f"{slug}.html").write_text(plate(n, **p))
    print(json.dumps({"event": "plate", "slug": slug}))

# Hero: the Phosphor-traced wordmark, then the six pin figures as an index.
labels = ["phosphor", "holographic-eye", "phosphor-mobil3", "bonsai27b-vulkan",
          "phosphor-mobil3-dev", "sysmon"]
index = "".join(
    f'<div class="ix"><img src="../img/sig{i}.png"><span>0{i}</span><em>{labels[i - 1]}</em></div>'
    for i in range(1, 7))
HERO = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1600px;height:640px;overflow:hidden;background:#000}}
body{{font-family:Inter,sans-serif;color:#f1edf1}}
.band{{position:absolute;left:0;top:0;width:1600px;height:500px;background:url(../img/hero-band.png) center/cover}}
.fade{{position:absolute;left:0;right:0;top:380px;height:120px;background:linear-gradient(transparent,#000)}}
.cap{{position:absolute;left:0;right:0;top:392px;text-align:center;font:500 19px/1 'JetBrains Mono',monospace;
  letter-spacing:.2em;color:rgba(107,255,140,.62);text-transform:uppercase}}
.strip{{position:absolute;left:40px;right:40px;top:452px;height:160px;display:flex;
  border-top:1px solid rgba(107,255,140,.18)}}
.ix{{flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;padding-top:18px;
  border-right:1px solid rgba(255,255,255,.07)}}
.ix:last-child{{border-right:0}}
.ix img{{width:78px;height:78px}}
.ix span{{font:600 16px/1 'JetBrains Mono',monospace;letter-spacing:.16em;color:rgba(241,237,241,.45)}}
.ix em{{font:500 18px/1 'JetBrains Mono',monospace;font-style:normal;color:rgba(241,237,241,.82)}}
</style></head><body>
<div class="band"></div><div class="fade"></div>
<div class="cap">traced by phosphor · left channel = x · right channel = y</div>
<div class="strip">{index}</div>
</body></html>"""
(OUT / "00-hero.html").write_text(HERO)
print(json.dumps({"event": "plate", "slug": "00-hero"}))
