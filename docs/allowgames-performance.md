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

### Conclusions so far

- On a 14700K + RTX 3070 the game reaches about 50 fps natively; the GPU is far from busy.
- The 60 fps lock (an even 30 plus 2x frame generation) is the steadiest way to a playable 60 today.
- Windows 10 on a hybrid Intel CPU is not the limit here (E-cores ruled out).
- Next to look at: the waits between `sead::MainThread` and the `ModuleSystemWorker` threads (`HOS_WAIT_LOG`, `HOS_SAMPLE`).

Results from other PCs are welcome: open an issue with your CPU, GPU, Windows version and the `vi: ... fps` and
`prof: busiest threads` lines of `hookshot_log.txt` (never game files).
