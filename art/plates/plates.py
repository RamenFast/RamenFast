#!/usr/bin/env python3
"""Build the profile hero and six pin plates as HTML, in Ben's pin order.

Every fact on a plate comes from the pinned repo's README, its release
list, or a recorded CLI reading (sysmon-gpu.json). Screenshots are the
repos' own, listed in art/SOURCES.md.
usage: ART_WORK=DIR plates.py   (reads DIR/img, writes DIR/html/*.html)
"""
import json
import os
import pathlib

WORK = pathlib.Path(os.environ["ART_WORK"])
OUT = WORK / "html"
OUT.mkdir(exist_ok=True)
GPU = json.loads((WORK / "sysmon-gpu.json").read_text())
GPU_DATE = GPU["read_at"][:10]

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
.text{position:absolute;left:64px;top:52px;width:660px;bottom:48px;display:flex;flex-direction:column}
.eyebrow{display:flex;align-items:center;gap:18px;font:600 21px/1 'JetBrains Mono',monospace;
  letter-spacing:.14em;color:var(--accent);text-transform:uppercase}
.eyebrow .sig{width:64px;height:64px;margin:-8px 0 -8px -6px}
.eyebrow .rule{flex:0 0 40px;height:1px;background:var(--accent);opacity:.6}
.eyebrow .stack{color:rgba(241,237,241,.55);letter-spacing:.1em}
h1{font:750 86px/1 Inter,sans-serif;letter-spacing:-.025em;margin-top:34px;white-space:nowrap}
.tag{font:400 31px/1.32 Inter,sans-serif;color:rgba(241,237,241,.76);margin-top:20px;max-width:640px}
.meta{margin-top:auto;font:500 20px/1 'JetBrains Mono',monospace;letter-spacing:.06em;
  color:rgba(241,237,241,.5);display:flex;gap:14px;align-items:center}
.meta b{color:var(--accent);font-weight:600}
.media{position:absolute;right:48px;top:44px;bottom:44px;left:780px;display:flex;gap:20px;
  justify-content:flex-end;align-items:stretch}
.shot{position:relative;border:1px solid var(--line-strong);background:#000;overflow:hidden;
  box-shadow:0 0 0 1px rgba(0,0,0,.6),0 30px 80px -30px var(--halo)}
.shot img{display:block;width:100%;height:100%;object-fit:cover}
.shot .cap{position:absolute;left:0;bottom:0;padding:7px 12px;background:rgba(0,0,0,.72);
  font:500 16px/1 'JetBrains Mono',monospace;letter-spacing:.06em;color:rgba(241,237,241,.72);
  border-top:1px solid var(--line);border-right:1px solid var(--line)}
.panel{border:1px solid var(--line-strong);background:rgba(0,0,0,.55);padding:26px 30px;
  font:500 21px/1.55 'JetBrains Mono',monospace;color:rgba(241,237,241,.82)}
.panel .k{color:rgba(241,237,241,.45)}
.panel .a{color:var(--accent)}
"""


def theme(r, g, b):
    rgb = f"{r},{g},{b}"
    return (f"--accent:rgb({rgb});--grid:rgba({rgb},.055);--halo:rgba({rgb},.16);"
            f"--line:rgba({rgb},.22);--line-strong:rgba({rgb},.38);"
            f"--bg:rgb({round(4 + r * .018)},{round(5 + g * .018)},{round(7 + b * .018)})")


def plate(n, accent, stack, name, tag, meta, media):
    sig = f"../img/sig{n}.png"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head>
<body><div class="plate" style="{theme(*accent)}">
<div class="glow"></div><div class="grid"></div><div class="frame"></div>
<div class="tick tl"></div><div class="tick tr"></div><div class="tick bl"></div><div class="tick br"></div>
<div class="text">
  <div class="eyebrow"><img class="sig" src="{sig}"><span>Pin 0{n}</span><span class="rule"></span><span class="stack">{stack}</span></div>
  <h1>{name}</h1>
  <p class="tag">{tag}</p>
  <div class="meta">{meta}</div>
</div>
<div class="media">{media}</div>
</div></body></html>"""


def shot(src, width, pos="center", cap=None):
    c = f'<span class="cap">{cap}</span>' if cap else ""
    return (f'<div class="shot" style="width:{width}px"><img src="../img/{src}" '
            f'style="object-position:{pos}">{c}</div>')


PLATES = [
    dict(slug="01-phosphor", accent=(107, 255, 140), stack="Rust · wgpu · PipeWire",
         name="Phosphor",
         tag="A GPU oscilloscope for everything your PC plays. Stereo in, light out.",
         meta="<b>v4.7.4</b><span>.deb · .rpm · GPLv3</span>",
         media=shot("ph-inuse.png", 740, "50% 30%", "live · XY · Attack Vector")),
    dict(slug="02-holographic-eye", accent=(231, 138, 166), stack="Rust · Tauri · Zig/WASM",
         name="Holographic Eye",
         tag="An agent's memory drawn as its real geometry. Journaled, undoable, yours.",
         meta="<b>v1.3.0</b><span>.deb · .rpm · GPLv3</span>",
         media=shot("he-hero.png", 740, "30% 40%", "synthetic demo data")),
    dict(slug="03-phosphor-mobile", accent=(89, 191, 255), stack="Kotlin · Compose · Rust",
         name="Phosphor Mobile",
         tag="The same beam engine in your pocket. 120&nbsp;Hz, edge to edge.",
         meta="<b>v1.0.7</b><span>signed APK · SHA256SUMS</span>",
         media=shot("pm-live.png", 300, "50% 50%", "kaleido · live")
         + shot("pm-dense.png", 300, "50% 50%", "kaleido · dense")),
    dict(slug="04-bonsai27b-vulkan", accent=(255, 158, 31), stack="Vulkan · llama.cpp · RDNA2",
         name="Bonsai 27B",
         tag="A 27B model on a 12 GB AMD card through plain Vulkan. No ROCm.",
         meta="<b>measured</b><span>RX 6750 XT · Mesa RADV · 2026-07-15</span>",
         media="""<div class="panel" style="width:740px">
<div><span class="k">model  </span> Ternary-Bonsai-27B</div>
<div><span class="k">weights</span> <span class="a">1.71</span> bits/weight · 7.17 GB</div>
<div><span class="k">decode </span> <span class="a">25–40</span> tok/s</div>
<div><span class="k">needle </span> <span class="a">5/5</span> at 43.5K tokens deep</div>
<div><span class="k">window </span> <span class="a">262K</span> native, KV spills to RAM</div>
<div style="margin-top:18px"><span class="k">vram   </span> 11.1 / 12 GB at 64K + vision</div>
<div style="margin-top:10px;height:14px;border:1px solid var(--line-strong);position:relative">
<div style="position:absolute;inset:2px auto 2px 2px;width:calc(92.5% - 4px);background:var(--accent);opacity:.85"></div></div>
</div>"""),
    dict(slug="05-phosphor-mobile-dev", accent=(255, 92, 92), stack="Kotlin · Rust · Tailscale",
         name="Mobile, dev line",
         tag="The open workbench. Features land, break and get fixed here first.",
         meta="<b>open</b><span>Discussions · CONTRIBUTING</span>",
         media=shot("pd-bestiary.png", 300, "50% 22%", "manual · the bestiary")
         + shot("pd-deck.png", 300, "50% 78%", "deck · remote PC")),
    dict(slug="06-sysmon", accent=(51, 255, 235), stack="Rust · egui · JSON API",
         name="SysMon",
         tag="A compact monitor for AMD-GPU Linux. Every number is one command away.",
         meta="<b>v3.0.3</b><span>.deb · .rpm · GPLv3</span>",
         media=f"""<div class="panel" style="width:430px;font-size:19px;line-height:1.6;align-self:center">
<div class="a">$ sysmon probe gpu --json</div>
<div class="k"># read {GPU_DATE}, 5 fields</div>
<div>&#123;</div>
<div>&nbsp; <span class="k">"busy_percent":</span> {GPU['busy_percent']},</div>
<div>&nbsp; <span class="k">"power_draw_watts":</span> {GPU['power_draw_watts']:g},</div>
<div>&nbsp; <span class="k">"power_cap_watts":</span> {GPU['power_cap_watts']:g},</div>
<div>&nbsp; <span class="k">"fan_rpm":</span> {GPU['fan_rpm']},</div>
<div>&nbsp; <span class="k">"core_clock_mhz":</span> {GPU['core_clock_mhz']:g}</div>
<div>&#125;</div>
</div>""" + shot("sm-overview.png", 290, "50% 0%", "overview")),
]

for p in PLATES:
    slug = p.pop("slug")
    n = int(slug[:2])
    (OUT / f"{slug}.html").write_text(plate(n, **p))
    print(json.dumps({"event": "plate", "slug": slug}))

# Hero: the Phosphor-traced wordmark, then the six pin figures as an index.
labels = ["Phosphor", "Holographic Eye", "Phosphor Mobile", "Bonsai 27B", "Mobile dev", "SysMon"]
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
.ix em{{font:500 19px/1 Inter,sans-serif;font-style:normal;color:rgba(241,237,241,.82)}}
</style></head><body>
<div class="band"></div><div class="fade"></div>
<div class="cap">traced by phosphor · left channel = x · right channel = y</div>
<div class="strip">{index}</div>
</body></html>"""
(OUT / "00-hero.html").write_text(HERO)
print(json.dumps({"event": "plate", "slug": "00-hero"}))
