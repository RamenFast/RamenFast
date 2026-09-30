<p align="center">
  <img src="assets/banner.png" alt="Four Phosphor beam renders: a heart, a Lissajous figure, a tunnel, a Takens embedding" width="100%">
</p>

<h1 align="center">Ben · RamenFast</h1>
<p align="center">I build instruments that let people <em>and</em> agents see the same thing.</p>

<p align="center">
  <a href="https://github.com/RamenFast/phosphor">Phosphor</a> ·
  <a href="https://github.com/RamenFast/phosphor-mobil3">Phosphor Mobile</a> ·
  <a href="https://github.com/RamenFast/sysmon">SysMon</a> ·
  <a href="https://github.com/RamenFast/cartograph">Cartograph</a> ·
  <a href="https://github.com/RamenFast/concourse">Concourse</a> ·
  <a href="https://github.com/RamenFast/intercom">Intercom</a>
</p>

---

### The station

Every tool here follows one rule: a human gets a real GUI, an agent gets a JSON CLI, and both talk to the same core. No screen-scraping, no second-class interface.

| | What it is | Stack |
|---|---|---|
| **[phosphor](https://github.com/RamenFast/phosphor)** | CRT-style XY oscilloscope for desktop audio. GPU beam, P7 phosphor physics, 11 display modes, drives Spotify from the transport. | Rust · wgpu · PipeWire |
| **[phosphor-mobil3](https://github.com/RamenFast/phosphor-mobil3)** | The same beam engine in your pocket. Playback capture, mic, Tailscale relay to the PC. Stable line. [Dev line →](https://github.com/RamenFast/phosphor-mobil3-dev) | Kotlin · Compose · Rust |
| **[sysmon](https://github.com/RamenFast/sysmon)** | Compact system monitor for AMD-GPU Linux. Live cards, pop-out windows, six themes, control socket. | Rust · egui |
| **[cartograph](https://github.com/RamenFast/cartograph)** | A living map of your machine's network. Every process and who it's talking to, by real name. | Zig · eBPF · GTK4 |
| **[concourse](https://github.com/RamenFast/concourse)** | The station's shared hall. One registry of every tool, one hub where human and agents see the same estate. | Rust · egui |
| **[intercom](https://github.com/RamenFast/intercom)** | Local two-way voice. piper TTS + whisper.cpp STT, CPU one-shots, pipelines into the local LLM. | Rust |

### Other things I've made

- **[zenfone9-root](https://github.com/RamenFast/zenfone9-root)** · temporary root on a bootloader-locked Zenfone 9 via CVE-2025-21479. C.
- **[bonsai27b-vulkan](https://github.com/RamenFast/bonsai27b-vulkan)** · a 27B ternary LLM on a 12GB RDNA2 card through Vulkan, no ROCm. First published RDNA2 numbers.
- **[holographic-eye](https://github.com/RamenFast/holographic-eye)** · an agent's memory drawn as its real holographic geometry. Undoable, themable.
- **[Blossom](https://github.com/RamenFast/Blossom)** · AMOLED true-black desktop theme, one palette engine for GTK, Cinnamon, icons, Steam. [Shell edition →](https://github.com/RamenFast/blossom-shell)
- **[iphone4s-retro](https://github.com/RamenFast/iphone4s-retro)** · bringing a family iPhone 4S back to iOS 6 entirely from Linux.

### How I work

Rust, Zig, Kotlin, and a lot of shell. AMD-GPU Linux, Sway. Everything I ship has a `--json` mode because my collaborators are agents as often as they're people. GPLv3 by default.

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=RamenFast&show_icons=true&theme=dark&hide_border=true&bg_color=00000000&title_color=ff9cc4&icon_color=ffd166&text_color=9ad0ff&hide_title=true&include_all_commits=true" alt="GitHub stats" height="150">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=RamenFast&layout=compact&theme=dark&hide_border=true&bg_color=00000000&title_color=ff9cc4&text_color=9ad0ff&langs_count=6" alt="Top languages" height="150">
</p>
