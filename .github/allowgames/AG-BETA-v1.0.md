## Hookshot · Allow Games Edition — AG BETA v1.0

**Source only. No game, no keys, no executable.** Build it on your PC from **your own legally owned copy**. Not affiliated with Nintendo.

### New
- **60 fps lock (on by default):** the game runs at an even 30 and 2x frame generation fills every other frame, evenly paced: a steady 60 on screen at real-time game speed. First row of the Insert menu.
- **Allow Games intro** at start (`ALLOWGAMES_NO_INTRO=1` in `hookshot_env.txt` skips it).
- **Edition version** in the window title and the Insert menu.
- Built on the latest upstream `main`, including EvilOOT's **black-flash (exposure flicker) fix**.

### How to build
1. Download `HookshotBuilder.zip`, extract it, run `HookshotBuilder.exe` (keep the `tools` folder beside it).
2. Choose your own `.nup` (or `romfs` + `exefs`), a language and a folder. Building over your old Hookshot folder keeps saves and settings.
3. Open `hookshot.exe`. Press **Insert** for the menu; turn on the FPS counter to check the 60.

Same requirements as upstream Hookshot (Windows 10/11, Vulkan 1.3 GPU with mesh shaders, 16 GB RAM, ~60 GB free while building, Visual Studio Build Tools with C++).

Credits: NotRexed (Hookshot), EvilBoyce/evilmfkr and every upstream contributor. Edition changes by AllGamersRD / Allow Games. GPL-3.0-or-later.
