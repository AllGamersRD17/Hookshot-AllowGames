## Hookshot · Allow Games Edition — AG BETA v1.2

**Source only. No game, no keys, no executable.** Build it from **your own legally owned copy**. Not affiliated with Nintendo.

### New
- **FPS lock: 30.** The first row of the Insert menu is now **FPS lock: Off / 60 / 30**. 30 holds the game to an even 30 with
  no frame generation: the lightest mode on the CPU and the GPU, like the console. 60 (the default) is unchanged: an even 30 plus
  2x frame generation. `ALLOWGAMES_LOCK60=2` in `hookshot_env.txt` starts at 30.

### Tip for 8 GB GPUs at 1440p
On an RTX 3070 at 2560x1440 the GPU took about 26 ms a frame with Resolution on Auto and VRAM ran over budget (6.8 of 6.2 GB),
so turning the camera dropped the game below 30 and Auto's resolution changes made the brightness pump. Set **Resolution
to 67%** (or 50%), or use the 30 lock. Details: [docs/allowgames-performance.md](../../docs/allowgames-performance.md).

### Updating
Download `HookshotBuilder.zip`, extract it to a new folder and build again into **the same game folder** with the same `.nup`:
saves and settings stay (a v1.0-v1.1 lock setting carries over). Delete the old builder folder afterwards.

Credits: NotRexed (Hookshot), EvilBoyce/evilmfkr and every upstream contributor. Edition changes by AllGamersRD / Allow Games. GPL-3.0-or-later.
