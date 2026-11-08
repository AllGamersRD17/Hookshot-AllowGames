"""Allow Games save tool: reads and writes Ocarina of Time (Switch 2) progress.sav (the TotK-style GameData save)."""
import struct

TYPES = ["Bool", "BoolArray", "Int", "IntArray", "Float", "FloatArray", "Enum", "EnumArray", "Vector2", "Vector2Array",
         "Vector3", "Vector3Array", "String16", "String16Array", "String32", "String32Array", "String64", "String64Array",
         "Binary", "BinaryArray", "UInt", "UIntArray", "Int64", "Int64Array", "UInt64", "UInt64Array", "WString16",
         "WString16Array", "WString32", "WString32Array", "WString64", "WString64Array", "Bool64bitKey"]

def mm3(key, seed=0):
    key = key.encode() if isinstance(key, str) else key
    h = seed; c1 = 0xcc9e2d51; c2 = 0x1b873593; n = len(key)
    for i in range(0, n // 4 * 4, 4):
        k = struct.unpack_from('<I', key, i)[0]
        k = (k * c1) & 0xffffffff; k = ((k << 15) | (k >> 17)) & 0xffffffff; k = (k * c2) & 0xffffffff
        h ^= k; h = ((h << 13) | (h >> 19)) & 0xffffffff; h = (h * 5 + 0xe6546b64) & 0xffffffff
    t = key[n // 4 * 4:]; k = 0
    for i, b in enumerate(t): k |= b << (8 * i)
    if t:
        k = (k * c1) & 0xffffffff; k = ((k << 15) | (k >> 17)) & 0xffffffff; k = (k * c2) & 0xffffffff; h ^= k
    h ^= n; h ^= h >> 16; h = (h * 0x85ebca6b) & 0xffffffff; h ^= h >> 13; h = (h * 0xc2b2ae35) & 0xffffffff; h ^= h >> 16
    return h

class Save:
    def __init__(self, data):
        self.d = bytearray(data)
        assert struct.unpack_from('<I', self.d, 0)[0] == 0x01020304, "not a progress.sav"
        self.data_off = struct.unpack_from('<I', self.d, 8)[0]
        self.entries = {}   # hash -> (type, slot offset in file)
        t = None
        for i in range(0x20, self.data_off, 8):
            h, v = struct.unpack_from('<II', self.d, i)
            if h == 0:
                t = v; continue
            self.entries[h] = (t, i)
    def type_of(self, name):
        e = self.entries.get(mm3(name) if isinstance(name, str) else name)
        return TYPES[e[0]] if e else None
    def raw(self, name):
        h = mm3(name) if isinstance(name, str) else name
        t, i = self.entries[h]
        return t, i, struct.unpack_from('<I', self.d, i + 4)[0]
    def get(self, name):
        t, i, v = self.raw(name)
        tn = TYPES[t]
        if tn in ("Bool", "Int", "UInt", "Enum"):
            return struct.unpack('<i', struct.pack('<I', v))[0] if tn == "Int" else v
        if tn == "Float":
            return struct.unpack('<f', struct.pack('<I', v))[0]
        return ("@", v)
    def set(self, name, value):
        t, i, v = self.raw(name)
        tn = TYPES[t]
        if tn == "Int": struct.pack_into('<i', self.d, i + 4, value)
        elif tn in ("UInt", "Enum", "Bool"): struct.pack_into('<I', self.d, i + 4, value)
        elif tn == "Float": struct.pack_into('<f', self.d, i + 4, value)
        else: raise ValueError(f"{name}: {tn} is not a single value")
