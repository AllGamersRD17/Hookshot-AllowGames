## Hookshot · Allow Games Edition — AG BETA v1.1

**Source only. No game, no keys, no executable.** Build it from **your own legally owned copy**. Not affiliated with Nintendo.

### Improved
- **Clearer picture:** the game's fog is thinned to 25% and exposure set to 90%, so outdoor scenes are no longer a white wall (tested in Kokiri Forest on an RTX 3070). `RX_VK_OOT_VISUAL=0` in `hookshot_env.txt` restores upstream's look; `RX_VK_OOT_FOG` / `RX_VK_OOT_EXPOSURE` set the amounts.
- **60 fps lock stays on:** changing Frame generation, Frame pacing or Game speed no longer switches the lock off by surprise (that brought back the uneven ~50 fps). Turn the lock off first to change them. Measured: the game at an exact 30.0, 60 on screen, 0 late frames.
- Rebased on the latest upstream `main`.

### Updating from v1.0
Download `HookshotBuilder.zip`, extract it over a new folder, and build again into **the same game folder** with the same `.nup`: saves and settings stay. Delete the old builder folder afterwards.

Credits: NotRexed (Hookshot), EvilBoyce/evilmfkr and every upstream contributor. Edition changes by AllGamersRD / Allow Games. GPL-3.0-or-later.
