## Hookshot · Allow Games Edition — AG BETA v1.5

**Source only. No game, no keys, no executable.** Build it from **your own legally owned copy**. Not affiliated with Nintendo.

### Fixed: brightness flashing outside (Hyrule Field)
Outdoors the picture flashed bright for single frames; caves and indoor areas looked fine. The game's CPU ran a frame ahead
of the GPU and rewrote data a pass still had to read, so the exposure meter saw a too-bright frame (issue 574 upstream,
about ten players on Windows). This release brings upstream's two fixes from today: each frame waits for its GPU work on
Windows too, and a capture waits only for the write-back of the page it copies (PR #645 by hckrman101), so the wait costs
little. `RX_VK_WAIT_GPU=-1` in `hookshot_env.txt` turns the wait off.

### Tips from our testing (8 GB GPUs)
- In open areas keep **Quality preset at Balanced** (8 GB) or lower: **Ultra** is meant for 16 GB+ and overflowed VRAM on an
  RTX 3070 in Hyrule Field (7.6 of 6.9 GB), dropping to 27-58 fps. Balanced + Resolution 75%: 60 fps with GPU at ~11 ms.
- FPS lock stays **off** by default (a native 60); set it to 60 or 30 in the Insert menu if your PC can't hold 60.
- All measurements: [docs/allowgames-performance.md](../../docs/allowgames-performance.md).

### Updating
Accept the game's update offer at start, or download `HookshotBuilder.zip` and build into the same game folder: saves and
settings stay.

Credits: NotRexed (Hookshot), hckrman101, EvilBoyce/evilmfkr and every upstream contributor. Edition changes by AllGamersRD / Allow Games. GPL-3.0-or-later.
