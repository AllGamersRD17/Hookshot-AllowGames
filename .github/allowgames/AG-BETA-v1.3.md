## Hookshot · Allow Games Edition — AG BETA v1.3

**Source only. No game, no keys, no executable.** Build it from **your own legally owned copy**. Not affiliated with Nintendo.

### Everything new in upstream Hookshot (up to `honest-eta`, 2026-11-08)
- **About 45% more fps** (PR #523: one fence timeline per NVN queue). Upstream measured 47 fps, up from 33, on an RTX 4060 Ti.
- **Fewer flickers and white flashes** (EvilBoyce's fix #296), missing geometry fixed on every GPU.
- **Real ultrawide** (21:9 and 32:9), **Quality presets** by VRAM, text speed, controller remapping, pads in the background.
- **No Visual Studio needed**: the builder brings its own compiler (llvm-mingw).
- Texture corruption in long sessions, AMD black screens, Intel compute pipelines, low-VRAM ASTC as BC3 and more.

### Allow Games Edition
- **FPS lock: Off / 60 / 30** stays the first row of the Insert menu (60 by default). With upstream's fps gain, try **Off** too:
  on a fast PC the game may now hold a native 60.
- **This edition's own HookshotBuilder.exe** is in the zip, so **the game's update offer works again**: from v1.3 on, the game
  tells you at start when a newer Allow Games Edition is out and updates itself (`ALLOWGAMES_UPDATE_CHECK=0` turns it off).
- Clearer picture (fog 25%, exposure 90%), the Allow Games intro and the edition version, as before.

### Updating
Download `HookshotBuilder.zip`, extract it to a new folder, run `HookshotBuilder.exe` and build into **the same game folder**:
saves and settings stay. Delete the old builder folder afterwards.

Credits: NotRexed (Hookshot), EvilBoyce/evilmfkr, hckrman101, klimovich008, nicholasgower and every upstream contributor.
Edition changes by AllGamersRD / Allow Games. GPL-3.0-or-later.
