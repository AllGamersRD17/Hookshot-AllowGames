## Hookshot · Allow Games Edition — AG BETA v1.6

**Source only. No game, no keys, no executable.** Build it from **your own legally owned copy**. Not affiliated with Nintendo.

### Nuevo: Allow Games Save Editor / New: Allow Games Save Editor
**ES:** Dale **todo** a una partida: 20 corazones, 999 rupias, magia, doble defensa, Guanteletes de Oro, las 3 espadas, los 3
escudos, todas las túnicas y botas, todos los objetos y máscaras, munición al máximo, 4 botellas (2 hadas, poción azul,
vacía), las 3 piedras, los 6 medallones y las 13 canciones. Cierra el juego y arrastra tu
`<juego>\user\save\<cuenta>\slot_NN\progress.sav` encima de `AllowGames-SaveEditor\AllowGames-SaveEditor.bat` (en este zip).
Siempre hace copia de seguridad primero. Probado en el juego.

**EN:** Gives a save slot **everything** (hearts, rupees, magic, defense, every sword, shield, tunic, boot, item and mask, full
ammo, bottles, stones, medallions, all songs). Close the game and drag your `progress.sav` onto
`AllowGames-SaveEditor\AllowGames-SaveEditor.bat`. A backup is always written first. Tested in game.

What we found to make it work: items appear only when their per-item **`StockNum`** is set (not just the `IsGet` flags); bag
and wallet limits sit in a capacity table; bottles need `IsValid` plus the content enum. Details and a full guide:
[tools/allowgames](https://github.com/AllGamersRD17/hookshot-allowgames/tree/allow-games/tools/allowgames).

Prior work: **Traiver's [OOT SW2SE](https://github.com/Traiver/OOT-SW2SE)** (a GUI editor for the same game) came out on
2026-11-07, a few hours before ours; we made ours independently.

### Also
- The menu shows **AG BETA v1.6**. Everything from v1.5 (no outdoor brightness flashes, native 60) is unchanged.

### Updating
Accept the game's update offer at start, or download `HookshotBuilder.zip` and build into the same game folder: saves and
settings stay.

Credits: NotRexed (Hookshot), hckrman101, EvilBoyce/evilmfkr, Traiver and every upstream contributor. Edition changes and the
save editor by AllGamersRD / Allow Games. GPL-3.0-or-later.
