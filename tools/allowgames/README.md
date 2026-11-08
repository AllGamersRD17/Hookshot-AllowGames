# Allow Games Save Editor

Gives a save slot everything: 999 rupees (Giant's Wallet), 20 hearts, magic and double defense, every weapon, shield, tunic,
boot, gauntlet, scale, mask, bag and ocarina, all items with full ammo (bombs 40, arrows 50, sticks 30, nuts 40, seeds 50,
bombchus 50, magic beans 10), 4 bottles (2 fairies, a blue potion, an empty one), the 3 spiritual stones, the 6 medallions,
the Gerudo card and the 13 songs. Trade-sequence items are left alone so quests keep working.

It edits only your own `progress.sav` and backs it up first (`progress.sav.bak-<time>`). It contains no game data: items
are found by the hashes of their names in the save.

```
python ag_save_editor.py "<game folder>\user\save\<account>\slot_01\progress.sav" all
python ag_save_editor.py "<...>\progress.sav" show
```
(The Hookshot Builder's `tools\python\python.exe` works if you have no Python.)

How it works: the game keeps each pouch item's `StockNum` in a per-item struct of the GameData list (ownership for weapons and
key items, the count for ammo), the bag and wallet limits in a capacity table, and bottles as `BottleInfo.BottleX.IsValid` +
`BottleItem`. Tested on AG BETA v1.5 (2026-11-08).
