# Allow Games Save Editor

**Por / By: Allow Games (AllGamersRD).** Hecho para **Hookshot · Allow Games Edition** (el port de PC de *The Legend of
Zelda: Ocarina of Time* para Switch 2). Made for **Hookshot · Allow Games Edition**.

> Sin archivos del juego, sin claves, sin datos de Nintendo. Edita **solo tus propias partidas**. No afiliado a Nintendo.
> No game files, no keys, no Nintendo data. Edits **only your own saves**. Not affiliated with Nintendo.

---

## Español

### Qué hace
Con un solo comando le da a una ranura de partida **todo**:

| | |
|---|---|
| **Vida y dinero** | 20 corazones (vida llena), 999 rupias con la Bolsa de Gigante |
| **Magia y defensa** | barra de magia, doble defensa |
| **Fuerza** | Guanteletes de Oro (levantar lo más pesado) |
| **Espadas** | Espada Kokiri, Espada Maestra, Espada de Biggoron |
| **Escudos** | Escudo Deku, Escudo Hyliano, Escudo Espejo |
| **Ropa y botas** | túnicas Kokiri, Goron y Zora; Botas de Hierro y Botas Levitadoras |
| **Objetos** | tirachinas, arco, boomerang, gancho y gancho largo, martillo, flechas de fuego/hielo/luz, ocarina del tiempo, lente de la verdad, caña de pescar, piedra de la agonía, escama de oro… |
| **Munición al máximo** | bombas 40, flechas 50, palos Deku 30, nueces 40, semillas 50, bombchus 50, judías mágicas 10, con las bolsas y el carcaj más grandes |
| **Botellas** | 4: dos hadas, una poción azul y una vacía |
| **Máscaras** | Keaton, Calavera, Espeluznante, Conejo, Goron, Zora, Gerudo, de la Verdad |
| **Misión** | las 3 piedras espirituales, los 6 medallones, la tarjeta Gerudo |
| **Canciones** | las 13 (Zelda, Epona, Saria, Sol, Tiempo, Tormentas, las 6 de teletransporte y la del espantapájaros) |

Se dejan como están, a propósito, los objetos de la cadena de intercambio (huevo, gallina, espada rota, etc.), para que esas
misiones sigan funcionando.

### Cómo se usa (fácil)
1. **Cierra el juego.**
2. Abre la carpeta de partidas: `<carpeta del juego>\user\save\<tu cuenta>\slot_NN\` (`slot_00`, `slot_01`… es el orden en
   que creaste las partidas).
3. Arrastra `progress.sav` encima de **`AllowGames-SaveEditor.bat`** (viene en la carpeta `AllowGames-SaveEditor` del
   `HookshotBuilder.zip`). Usa el Python que trae el Builder; no tienes que instalar nada.
4. Abre el juego y carga esa partida.

Siempre se guarda una copia antes: `progress.sav.bak-<fecha>`. Para volver atrás, borra `progress.sav` y quita
`.bak-<fecha>` al nombre de la copia.

### Comandos (avanzado)
```
python ag_save_editor.py "<...>\slot_01\progress.sav" all        (todo)
python ag_save_editor.py "<...>\progress.sav" show               (ver lo que tiene)
python ag_save_editor.py "<...>\progress.sav" rupees 500
python ag_save_editor.py "<...>\progress.sav" hearts 12
```
También: `items`, `songs`, `quest`, `masks`, `equipment`, `bottles`, `magic`, `strength`, `defense`.

### ¿Funciona en la Switch 2 o en un emulador?
El formato del archivo es el del juego de Switch 2, así que el mismo `progress.sav` debería servir en un emulador que lo
corra. **Solo lo hemos probado en Hookshot (PC)**. En una consola tendrías que sacar y volver a meter la partida tú mismo
(eso no lo cubrimos). Haz siempre copia.

---

## English

### What it does
One command gives a save slot **everything**: 20 hearts, 999 rupees (Giant's Wallet), magic, double defense, Golden
Gauntlets; Kokiri, Master and Biggoron swords; Deku, Hylian and Mirror shields; all tunics and boots; every item (slingshot,
bow, boomerang, hookshot and longshot, hammer, fire/ice/light arrows, Ocarina of Time, Lens of Truth, fishing rod, Stone of
Agony, gold scale…) with full ammo and the largest bags and quiver (bombs 40, arrows 50, sticks 30, nuts 40, seeds 50,
bombchus 50, magic beans 10); 4 bottles (two fairies, a blue potion, an empty one); 8 masks; the 3 spiritual stones, the 6
medallions, the Gerudo card and all 13 songs. Trade-sequence items are left alone so those quests still work.

### Use
Close the game, drag `<game folder>\user\save\<account>\slot_NN\progress.sav` onto `AllowGames-SaveEditor.bat`, start the
game and load that slot. A backup (`progress.sav.bak-<time>`) is always written first. Command line: see above (`all`,
`show`, `rupees N`, `hearts N`, `items`, `songs`, `quest`, `masks`, `equipment`, `bottles`, `magic`, `strength`,
`defense`).

Same file format as the Switch 2 game, so the edited save should work in an emulator too; **tested only on Hookshot (PC)**.

---

## How it works (what we found)

The save is the same GameData format as other recent Switch Zelda titles: a header (magic `0x01020304`) and tables of
`(hash, value)` pairs grouped by type, where each hash is **murmur3-32 (seed 0)** of the flag's name, and arrays point to
absolute offsets. What made this editor work, and what we worked out ourselves on 2026-11-08:

- **Setting the `IsGet.*` flags is not enough.** Items only show up in the menus when their **`StockNum`** is set. Each pouch
  item has its own struct in the game's GameData list (`romfs/GameData/GameDataList.Product.110.byml.zs`, a BYML v7
  compressed with the game's own zstd dictionaries), and that struct maps member names to the flag hashes of that item's
  `StockNum`. We read that list from **our own dumped game** and kept **only the resulting name→hash table** (in the
  editor), never the game file. For weapons and key items `StockNum` means owned; for ammo it is the count.
- **Bag, quiver and wallet limits** live in a separate capacity table; ammo above the limit is clamped by the game, so the
  editor raises the bag first.
- **Bottles** need `BottleInfo.BottleA..D.IsValid` plus a `BottleItem` enum, stored as `mm3("Fairy")`, `mm3("BluePotion")`,
  `mm3("Empty")`.
- Enums in general (e.g. `LiftGrade = mm3("High")` for the Golden Gauntlets) are stored as the hash of the value's name.
- Songs are given through `IsGet.Item_Melody_*`.

Tested in game on AG BETA v1.5 (items, ammo, bottles, equipment and the collection screen checked by eye).

## Credits and prior work

- **Allow Games (AllGamersRD)**: this editor, the `StockNum`/capacity/bottle findings above and the Hookshot integration.
- **Traiver — [OOT SW2SE](https://github.com/Traiver/OOT-SW2SE)**: another save editor for the same game (a Windows app with a
  graphical editor), published on 2026-11-07, a few hours before ours. We built ours on our own without knowing of it. If you
  want a GUI, try theirs too.
- **NotRexed — [Hookshot](https://github.com/NotRexed/Hookshot)**, the recompilation this edition is built on, and every
  upstream contributor.
- The GameData save layout was first documented by the *Tears of the Kingdom* modding community (e.g. turtle-insect's
  ZeldaTOTK editor).

GPL-3.0-or-later, like the rest of the repository.
