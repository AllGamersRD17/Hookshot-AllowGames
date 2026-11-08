# Allow Games Edition: performance notes

Measurements made on players' PCs while working toward a native 60 fps. Published so nobody has to repeat them.

## Test PC 1 (2026-11-07)

Intel Core i7-14700K (8 P-cores + 12 E-cores, 28 threads), NVIDIA RTX 3070, Windows 10 22H2 (build 19045).
Kokiri Forest, walking. Build AG BETA v1.0/v1.1.

| Setup | Game frame rate | On screen | Notes |
|---|---|---|---|
| Upstream defaults (no lock, frame generation 2x) | 45-51 fps, uneven | ~99 | the swings are felt as stutter |
| **60 fps lock (the edition's default)** | **30.0 exact** | **60** | 0 late frames over minutes of play |
| Game threads pinned to the 8 P-cores only (`HOS_PIN=*=FFFF`) | 49-52 fps | ~100 | no real gain, and the player found it felt worse: not kept |

### What `HOS_PROFILE=10` showed (no lock, P-cores only)

Busiest threads, % of one core: `sead::MainThread` 67, `ModuleSystemWorker1-5` 60-63 each, `Presentation Thread` 29,
`BaseProcExecutor0-2` 12-14; about 5 cores busy in total.

No thread is at 100%: the game is **not** limited by any one core being too slow. Its threads spend the rest of each frame
waiting for each other (the main thread and the five module workers hand work back and forth), so a faster or less busy
core does not shorten the frame. That is why pinning to P-cores changed nothing, and why a native 60 needs work on how the
recompiled game's threads synchronise (host/hos_svc.c, host/nn_os_sync.c, the virtual cores in host/hos_thread.c), not on
which cores they run.

### GPU limit at 1440p (later the same day)

At 2560x1440 with Resolution on Auto, in Kokiri Forest: GPU time 25-27 ms a frame and VRAM over budget (6822 MB used of
6246 MB allowed, textures 2.2 GB of a 1.5 GB budget). With the 60 lock the game fell to 20-29 fps when turning the camera
(new textures not fitting), and the brightness pumped as Auto changed the resolution. Next: Resolution 67%, and the new 30
lock (AG BETA v1.2) for the lightest load.

### AG BETA v1.3: a native 60 (2026-11-08)

With upstream's per-queue fences (about 45% more fps) in the edition, on the same PC (14700K, RTX 3070, 2560x1440, Quality
preset Balanced, Resolution 100%, Handheld profile off, **FPS lock off, frame generation off**): **60.0 fps native**, every
5-second window at 60.0; present intervals 15.5-17.8 ms for ~87% of frames and none over 22 ms; GPU 12.6-13.2 ms a frame.
The player described it as completely smooth with no stutter. From AG BETA v1.4 the FPS lock is off by default.

### Hyrule Field on an 8 GB card (2026-11-08)

Out in Hyrule Field with Quality preset **Ultra** (meant for 16 GB+) on the RTX 3070 (8 GB) at 1440p and Resolution 100%: 3,800
draws a frame (Kokiri: ~1,000), GPU 18-19 ms, VRAM over budget (7.6 GB used of 6.9 GB allowed, textures 3.0 GB of a 2.2 GB
budget). The game fell to 27-58 fps and the brightness flashed. Next: Quality preset **Balanced** (8 GB) and Resolution 75%;
On Balanced (Handheld profile on, Resolution 75%): 60 fps with GPU at 10-11 ms. The remaining outdoor brightness flashes were upstream issue 574 (CPU a frame ahead of the GPU), fixed in AG BETA v1.5 by the per-frame GPU wait. On 8 GB cards, keep the preset at Balanced or lower.

### Conclusions so far

- On a 14700K + RTX 3070 the game reaches about 50 fps natively; the GPU is far from busy.
- Before v1.3: the 60 fps lock (an even 30 plus 2x frame generation) was the steadiest way to 60. From v1.3 a native 60 holds on this PC; the lock (60 or 30) stays for slower PCs.
- Windows 10 on a hybrid Intel CPU is not the limit here (E-cores ruled out).
- Next to look at: the waits between `sead::MainThread` and the `ModuleSystemWorker` threads (`HOS_WAIT_LOG`, `HOS_SAMPLE`).

Results from other PCs are welcome: open an issue with your CPU, GPU, Windows version and the `vi: ... fps` and
`prof: busiest threads` lines of `hookshot_log.txt` (never game files).
