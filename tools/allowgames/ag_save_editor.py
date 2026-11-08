#!/usr/bin/env python3
r"""Allow Games Save Editor for Hookshot (Ocarina of Time, Switch 2 data).

Edits a slot's progress.sav: rupees, hearts, magic, strength, double defense and every item, song, stone and medallion.
A backup of the slot is written beside it first (progress.sav.bak-<time>). Works on YOUR saves only; it ships no game data.

Where the saves are: <game folder>\user\save\<account>\slot_NN\progress.sav (slot_00 is the first slot in the Load list
order of creation, not of date). Close the game, or use the in-game Load after editing, and never Save over the edited slot
from an older game session.

Usage:
  python ag_save_editor.py <progress.sav> show
  python ag_save_editor.py <progress.sav> all          (everything below)
  python ag_save_editor.py <progress.sav> rupees 999 | hearts 20 | items | songs | quest | masks | equipment | bottles | magic 96 | strength 3 | defense
"""
import os, sys, time, shutil, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsave import Save, mm3

ITEMS = ["Item_DekuStick", "Item_DekuNut", "Item_DekuSeed", "Item_Bomb", "Item_Bombchu", "Item_Boomerang", "Item_Hookshot",
         "Item_Longshot", "Item_Hammer", "Item_Bottle", "Item_Arrow_Normal", "Item_Arrow_Fire", "Item_Arrow_Ice", "Item_Arrow_Light",
         "Item_Ocarina_Fairy", "Item_Ocarina_Time", "Item_FishingRod", "Weapon_Range_Bow", "Weapon_Range_SlingShot", "Armor_GlassTruth",
         "Item_StickBag_Large", "Item_NutBag_Large", "Item_BulletBag_Large", "Item_BombBag_Large", "Item_Quiver_Large",
         "Item_Wallet_Large", "Item_Scale_Gold", "Item_AgonyStone"]
SONGS = ["Item_Melody_ZeldaLullaby", "Item_Melody_EponaSong", "Item_Melody_SariaSong", "Item_Melody_SunSong", "Item_Melody_TimeSong",
         "Item_Melody_StormSong", "Item_Melody_ForestMinuet", "Item_Melody_FireBolero", "Item_Melody_WaterSerenade",
         "Item_Melody_ShadowNocturne", "Item_Melody_SpiritRequiem", "Item_Melody_LightPrelude", "Item_Melody_ScarecrowSong"]
QUEST = ["Item_Stone_Forest", "Item_Stone_Fire", "Item_Stone_Water", "Item_Medal_Forest", "Item_Medal_Fire", "Item_Medal_Water",
         "Item_Medal_Spirit", "Item_Medal_Shadow", "Item_Medal_Light", "Item_Token_Gerudo"]
MASKS = ["Armor_Child_Mask_Keaton", "Armor_Child_Mask_Skull", "Armor_Child_Mask_Spooky", "Armor_Child_Mask_Bunny",
         "Armor_Child_Mask_Goron", "Armor_Child_Mask_Zora", "Armor_Child_Mask_Gerudo", "Armor_Child_Mask_Truth"]
EQUIPMENT = ["Weapon_Sword_Kokiri", "Weapon_Sword_Master", "Weapon_Sword_Biggoron", "Weapon_Shield_Deku", "Weapon_Shield_Hylian",
             "Weapon_Shield_Mirror", "Armor_Adult_Normal", "Armor_Adult_Goron", "Armor_Adult_Zora", "Armor_Adult_HeavyBoot",
             "Armor_Adult_HoverBoot", "Armor_Child_Gauntlet_Goron", "Armor_Adult_Gauntlet_Silver", "Armor_Adult_Gauntlet_Gold"]
# smaller upgrades are kept too: the game may check them in order
UPGRADES = ["Item_StickBag_Small", "Item_StickBag_Medium", "Item_NutBag_Small", "Item_NutBag_Medium", "Item_BulletBag_Small",
            "Item_BulletBag_Medium", "Item_BombBag_Small", "Item_BombBag_Medium", "Item_Quiver_Small", "Item_Quiver_Medium",
            "Item_Wallet_Small", "Item_Wallet_Medium", "Item_Scale_Silver"]


# Each pouch item's StockNum (the GameDataList's per-item struct: the item menus read it). Hashes, so no game data is shipped.
STOCK = {"Armor_Adult_Gauntlet_Gold": 1085149571, "Armor_Adult_Gauntlet_Silver": 1226944, "Armor_Adult_Goron": 569163033, "Armor_Adult_HeavyBoot": 732764314, "Armor_Adult_HoverBoot": 3374449510, "Armor_Adult_Normal": 1868764040, "Armor_Adult_Zora": 3088494484, "Armor_Child_Gauntlet_Goron": 3509680449, "Armor_Child_Mask_Amiibo0": 4125509594, "Armor_Child_Mask_Amiibo1": 1215060388, "Armor_Child_Mask_Bunny": 2120249395, "Armor_Child_Mask_Gerudo": 244623583, "Armor_Child_Mask_Goron": 4233137575, "Armor_Child_Mask_Keaton": 3049326745, "Armor_Child_Mask_Skull": 1202902901, "Armor_Child_Mask_Spooky": 4031144606, "Armor_Child_Mask_Truth": 2521144531, "Armor_Child_Mask_Zora": 2454624838, "Armor_GlassTruth": 1238483828, "BottleA": 3577537447, "BottleB": 4238514692, "BottleC": 2301761185, "BottleD": 1394932179, "BottleE": 3375044286, "Item_AgonyStone": 4088483042, "Item_AlarmCucco": 3066716307, "Item_Arrow_Fire": 1582471865, "Item_Arrow_Ice": 1081301645, "Item_Arrow_Light": 3216147912, "Item_Arrow_Normal": 1368311627, "Item_Bomb": 3676032335, "Item_BombBag_Large": 3174867654, "Item_BombBag_Medium": 3858711978, "Item_BombBag_Small": 2963390289, "Item_Bombchu": 3749466490, "Item_Boomerang": 2715249969, "Item_BrokenSword": 672516138, "Item_BulletBag_Large": 2073457653, "Item_BulletBag_Medium": 2586880485, "Item_BulletBag_Small": 3696405679, "Item_ClaimCheck": 3738757331, "Item_CojiroCucco": 1373150960, "Item_DekuNut": 4077756244, "Item_DekuSeed": 1605236732, "Item_DekuStick": 3108586513, "Item_DinFire": 3080110445, "Item_EyeballFrog": 2443092772, "Item_EyeDrop": 1547806385, "Item_FairyBless_DefenseDouble": 2592239531, "Item_FairyBless_MP": 1583816082, "Item_FairyBless_MPDouble": 1594112086, "Item_FaroreWind": 1207093895, "Item_Hammer": 447732582, "Item_Hookshot": 2238960333, "Item_Longshot": 2224679476, "Item_MagicBean": 2952991309, "Item_Medal_Fire": 1558336678, "Item_Medal_Forest": 1764579275, "Item_Medal_Light": 593264026, "Item_Medal_Shadow": 541925475, "Item_Medal_Spirit": 209346512, "Item_Medal_Water": 22128271, "Item_NayruLove": 4035087568, "Item_NormalBoot": 1441268958, "Item_NutBag_Large": 3591260963, "Item_NutBag_Medium": 3936450654, "Item_NutBag_Small": 431492540, "Item_Ocarina_Fairy": 3084869873, "Item_Ocarina_Time": 1424139217, "Item_OddMushroom": 132005487, "Item_OddPowder": 1489615992, "Item_PoacherSaw": 2825048694, "Item_PocketCucco": 23455690, "Item_PocketEgg": 133237423, "Item_Prescription": 2306668523, "Item_Quiver_Large": 3543255002, "Item_Quiver_Medium": 1001615585, "Item_Quiver_Small": 2831409659, "Item_Scale_Gold": 1256920074, "Item_Scale_Silver": 306185291, "Item_ScrubBusinessSeed": 1611540971, "Item_StickBag_Large": 1222981272, "Item_StickBag_Medium": 1104902837, "Item_StickBag_Small": 803646234, "Item_Stone_Fire": 2104077639, "Item_Stone_Forest": 3419530636, "Item_Stone_Water": 3101933381, "Item_Token_Gerudo": 4273263979, "Item_Token_Gold": 74668408, "Item_Wallet_Large": 2946808658, "Item_Wallet_Medium": 757892939, "Item_Wallet_Small": 494166398, "Item_WeirdEgg": 609840782, "Item_ZeldaLetter": 1810219952, "Obj_Armor_Child_Normal": 2226785572, "Obj_Heart_Piece": 1374459827, "Pouch_Amiibo": 545391737, "Pouch_Range_BowAndArrow_Fire": 3811234319, "Pouch_Range_BowAndArrow_Ice": 1719434147, "Pouch_Range_BowAndArrow_Light": 673809031, "Weapon_Range_Bow": 2475513535, "Weapon_Range_SlingShot": 2161331433, "Weapon_Shield_Deku": 2091274019, "Weapon_Shield_Hylian": 146734394, "Weapon_Shield_Mirror": 4119727663, "Weapon_Sword_Biggoron": 2964579225, "Weapon_Sword_BrokenGiant": 2365781482, "Weapon_Sword_Giant": 963271682, "Weapon_Sword_Kokiri": 4004812217, "Weapon_Sword_Master": 4056175252}
# Capacity table: wallet and ammo maximums (the menus show "as many as N")
CAP = {"Rupee": 3758164560, "Seed": 2928461634, "Bomb": 3880997003, "Arrow": 1099806609, "DekuStick": 1165366960, "DekuNut": 1935343863}
# BottleX.IsValid (PlayerStatus.AssignableItem.BottleInfo.BottleX struct member)
STRUCT_BOTTLE_VALID = {"A": 4087145488, "B": 1046250, "C": 4131066260, "D": 3085980366}
CONSUMABLES = {"Item_Bomb": ("Bomb", 40), "Item_Arrow_Normal": ("Arrow", 50), "Item_DekuStick": ("DekuStick", 30),
               "Item_DekuNut": ("DekuNut", 40), "Item_DekuSeed": ("Seed", 50), "Item_Bombchu": (None, 50), "Item_MagicBean": (None, 10)}
SKIP = {"Item_AlarmCucco", "Item_PocketEgg", "Item_PocketCucco", "Item_CojiroCucco", "Item_OddMushroom", "Item_OddPowder",
        "Item_PoacherSaw", "Item_BrokenSword", "Item_Prescription", "Item_EyeballFrog", "Item_EyeDrop", "Item_ClaimCheck",
        "Item_WeirdEgg", "Item_ZeldaLetter", "Item_ScrubBusinessSeed", "Armor_Child_Mask_Amiibo0", "Armor_Child_Mask_Amiibo1",
        "Pouch_Amiibo", "Obj_Heart_Piece", "Weapon_Sword_BrokenGiant", "Weapon_Sword_Giant", "BottleE", "Item_Token_Gold",
        "Item_NormalBoot", "Obj_Armor_Child_Normal"}

def set_stock(s, name, n):
    h = STOCK.get(name)
    if h is not None and s.type_of(h) == "Int":
        s.set(h, n); return True
    return False

def give_all_pouch(s, group):
    n = 0
    for name in STOCK:
        if name in SKIP: continue
        cat = ("quest" if name.startswith(("Item_Medal", "Item_Stone", "Item_Token_Gerudo")) else
               "masks" if "Mask" in name else
               "equipment" if name.startswith(("Weapon_Sword", "Weapon_Shield", "Armor_")) else "items")
        if group not in ("all", cat): continue
        if name in CONSUMABLES:
            capname, mx = CONSUMABLES[name]
            n += set_stock(s, name, mx)
        else:
            n += set_stock(s, name, 1)
        k = "IsGet." + name
        if s.type_of(k) == "Bool": s.set(k, 1)
    if group in ("all", "items"):
        for capname, mx in (("Rupee", 999), ("Seed", 50), ("Bomb", 40), ("Arrow", 50), ("DekuStick", 30), ("DekuNut", 40)):
            if s.type_of(CAP[capname]) == "Int": s.set(CAP[capname], mx)
    return n

def give(s, names):
    done = []
    for n in names:
        k = "IsGet." + n
        if s.type_of(k) == "Bool":
            s.set(k, 1); done.append(n)
    return done

def main():
    if len(sys.argv) < 3: print(__doc__); return 1
    path, cmd, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    s = Save(open(path, "rb").read())
    if cmd == "show":
        for k in ["PlayerStatus.CurrentRupee", "PlayerStatus.Life", "PlayerStatus.MaxLife", "PlayerStatus.MPMax",
                  "PlayerStatus.LiftGrade", "PlayerStatus.IsDefenseUP"]:
            print(f"{k}: {s.get(k)}")
        got = [n for n in ITEMS + UPGRADES + SONGS + QUEST + MASKS + EQUIPMENT if s.type_of("IsGet." + n) and s.get("IsGet." + n)]
        print("has:", ", ".join(got))
        return 0
    bak = f"{path}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copy2(path, bak)
    print("backup:", bak)
    if cmd in ("rupees", "all"):
        s.set("PlayerStatus.CurrentRupee", int(args[0]) if cmd == "rupees" else 999)
    if cmd in ("hearts", "all"):
        q = 4 * (int(args[0]) if cmd == "hearts" else 20)
        s.set("PlayerStatus.MaxLife", q); s.set("PlayerStatus.Life", q)
    if cmd in ("strength", "all"):
        s.set("PlayerStatus.LiftGrade", [0, mm3("Low"), mm3("Middle"), mm3("High")][int(args[0]) if cmd == "strength" else 3])
    if cmd in ("bottles", "all"):
        for b, item in zip("ABCD", ("Fairy", "Fairy", "BluePotion", "Empty")):
            s.set(f"PlayerStatus.AssignableItem.BottleInfo.Bottle{b}.BottleItem", mm3(item))
            s.set(STRUCT_BOTTLE_VALID[b], 1)
    if cmd in ("magic", "all"):
        mp = int(args[0]) if cmd == "magic" else 96
        s.set("PlayerStatus.MPMax", mp); s.set("PlayerStatus.MP", mp)
    if cmd in ("defense", "all"):
        s.set("PlayerStatus.IsDefenseUP", 1)
    if cmd in ("items", "all"): print("items:", give_all_pouch(s, "items"), len(give(s, ITEMS + UPGRADES)))
    if cmd in ("songs", "all"): print("songs:", len(give(s, SONGS)))
    if cmd in ("quest", "all"): print("quest:", give_all_pouch(s, "quest"), len(give(s, QUEST)))
    if cmd in ("masks", "all"): print("masks:", give_all_pouch(s, "masks"), len(give(s, MASKS)))
    if cmd in ("equipment", "all"): print("equipment:", give_all_pouch(s, "equipment"), len(give(s, EQUIPMENT)))
    open(path, "wb").write(s.d)
    print("saved:", path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
