import numpy as np
import sys
np.set_printoptions(threshold=np.inf, linewidth=30000)
np.set_printoptions(threshold=sys.maxsize)
#from PIL import Image as im
from ReadWriteMemory import ReadWriteMemory
import pymem
from enum import Enum, unique

#pm = pymem.Pymem("PD.exe")
#rwm = ReadWriteMemory()

#pm = pymem.Pymem("PD.exe")
#rwm = ReadWriteMemory()

# 04/10/2021 - início do projeto (pesquisa)
# 13/10/2021 - início do desenvolvimento do código

@unique
class StaticTileType(Enum):
    CHASM = 0
    EMPTY = 1
    GRASS = 2
    EMPTY_WELL = 3
    WALL = 4
    DOOR = 5
    OPEN_DOOR = 6
    ENTRANCE = 7
    EXIT = 8
    EMBERS = 9
    LOCKED_DOOR = 10
    PEDESTAL = 11
    WALL_DECO = 12
    BARRICADE = 13
    EMPTY_SP = 14
    HIGH_GRASS = 15
    EMPTY_DECO = 24
    LOCKED_EXIT = 25
    UNLOCKED_EXIT = 26
    SIGN = 29
    WELL = 34
    STATUE = 35
    STATUE_SP = 36
    BOOKSHELF = 41
    ALCHEMY = 42
    CHASM_FLOOR = 43
    CHASM_FLOOR_SP = 44
    CHASM_WALL = 45
    CHASM_WATER = 46
    SECRET_DOOR = 16
    TOXIC_TRAP = 17
    SECRET_TOXIC_TRAP = 18
    FIRE_TRAP = 19
    SECRET_FIRE_TRAP = 20
    PARALYTIC_TRAP = 21
    SECRET_PARALYTIC_TRAP = 22
    INACTIVE_TRAP = 23
    POISON_TRAP = 27
    SECRET_POISON_TRAP = 28
    ALARM_TRAP = 30
    SECRET_ALARM_TRAP = 31
    LIGHTNING_TRAP = 32
    SECRET_LIGHTNING_TRAP = 33
    GRIPPING_TRAP = 37
    SECRET_GRIPPING_TRAP = 38
    SUMMONING_TRAP = 39
    SECRET_SUMMONING_TRAP = 40
    WATER_TILES = 48
    WATER = 63
    UNKNOWN_1 = 49
    UNKNOWN_2 = 60
    UNKNOWN_3 = 54
    UNKNOWN_4 = 57
    WATER_4 = 62
    #WATER_4 = 63
    UNKNOWN_6 = 51
    UNKNOWN_7 = 55
    UNKNOWN_8 = 61
    WATER_3 = 59
    UNKNOWN_10 = 50
    UNKNOWN_11 = 52
    WATER_2 = 53
    UNKNOWN_13 = 58
    UNKNOWN_14 = 56

def utilsTileTypes():
    goodTiles = [0, 7, 8, StaticTileType.EMPTY.value, StaticTileType.GRASS.value, StaticTileType.HIGH_GRASS.value, StaticTileType.DOOR.value, StaticTileType.OPEN_DOOR.value,
                 StaticTileType.WATER.value, StaticTileType.WATER_2.value, StaticTileType.WATER_3.value, StaticTileType.WATER_4.value, StaticTileType.WATER_TILES.value,
                 StaticTileType.EXIT.value, StaticTileType.UNLOCKED_EXIT.value]  # tiles que retornam reward quando personagem caminha neles

    badTiles = [4, StaticTileType.WALL.value, StaticTileType.WALL_DECO.value, StaticTileType.LOCKED_DOOR.value, StaticTileType.LOCKED_EXIT.value,
                StaticTileType.WELL.value, StaticTileType.EMPTY_WELL.value]  # tiles que retornam penalização

    worstTiles = [5, StaticTileType.SIGN.value, StaticTileType.ENTRANCE.value]  # tiles que se der use tranca o jogo ou volta pro nível anterior

    lockTiles = [2, StaticTileType.CHASM_WALL.value, StaticTileType.CHASM_WATER.value, StaticTileType.CHASM_FLOOR.value,
                 StaticTileType.CHASM_FLOOR_SP.value]  # tiles que trancam o jogo com uma mensagem

    #lockTiles = [2, StaticTileType.CHASM.value, StaticTileType.CHASM_WALL.value, StaticTileType.CHASM_WATER.value, StaticTileType.CHASM_FLOOR.value,
                 #StaticTileType.CHASM_FLOOR_SP.value]

    goalTiles = [8, StaticTileType.EXIT.value, StaticTileType.UNLOCKED_EXIT.value]  # tile escada próx. nível



    return goodTiles, badTiles, worstTiles, lockTiles, goalTiles


class ColorMap(Enum):
    CHASM = (51, 255, 255)
    EMPTY = (215, 215, 215)
    GRASS = (0, 147, 55)
    EMPTY_WELL = (255, 255, 255)
    WALL = (150, 150, 150)
    DOOR = (117, 86, 42)
    OPEN_DOOR = (205, 167, 116)
    ENTRANCE = (58, 58, 58)
    EXIT = (58, 58, 58)
    EMBERS = (255, 255, 255)
    LOCKED_DOOR = (255, 255, 255)
    PEDESTAL = (255, 255, 255)
    WALL_DECO = (255, 255, 255)
    BARRICADE = (255, 255, 255)
    EMPTY_SP = (255, 255, 255)
    HIGH_GRASS = (0, 147, 55)
    EMPTY_DECO = (255, 255, 255)
    LOCKED_EXIT = (255, 255, 255)
    UNLOCKED_EXIT = (255, 255, 255)
    SIGN = (224, 107, 195)
    WELL = (255, 255, 255)
    STATUE = (255, 255, 255)
    STATUE_SP = (255, 255, 255)
    BOOKSHELF = (255, 255, 255)
    ALCHEMY = (255, 255, 255)
    CHASM_FLOOR = (255, 255, 255)
    CHASM_FLOOR_SP = (255, 255, 255)
    CHASM_WALL = (255, 255, 255)
    CHASM_WATER = (255, 255, 255)
    SECRET_DOOR = (255, 255, 255)
    TOXIC_TRAP = (255, 128, 0)
    SECRET_TOXIC_TRAP = (255, 128, 0)
    FIRE_TRAP = (255, 128, 0)
    SECRET_FIRE_TRAP = (255, 128, 0)
    PARALYTIC_TRAP = (255, 128, 0)
    SECRET_PARALYTIC_TRAP = (255, 128, 0)
    INACTIVE_TRAP = (255, 255, 255)
    POISON_TRAP = (255, 128, 0)
    SECRET_POISON_TRAP = (255, 128, 0)
    ALARM_TRAP = (255, 128, 0)
    SECRET_ALARM_TRAP = (255, 128, 0)
    LIGHTNING_TRAP = (255, 128, 0)
    SECRET_LIGHTNING_TRAP = (255, 128, 0)
    GRIPPING_TRAP = (255, 128, 0)
    SECRET_GRIPPING_TRAP = (255, 128, 0)
    SUMMONING_TRAP = (255, 128, 0)
    SECRET_SUMMONING_TRAP = (255, 128, 0)
    WATER_TILES = (75, 109, 92)
    WATER = (212, 241, 249)
    UNKNOWN_1 = (51, 255, 255)
    UNKNOWN_2 = (51, 255, 255)
    UNKNOWN_3 = (51, 255, 255)
    UNKNOWN_4 = (51, 255, 255)
    WATER_4 = (200, 200, 200)
    UNKNOWN_6 = (51, 255, 255)
    UNKNOWN_7 = (51, 255, 255)
    UNKNOWN_8 = (51, 255, 255)
    WATER_3 = (200, 200, 200)
    UNKNOWN_10 = (51, 255, 255)
    UNKNOWN_11 = (51, 255, 255)
    WATER_2 = (200, 200, 200)
    UNKNOWN_13 = (51, 255, 255)
    UNKNOWN_14 = (51, 255, 255)

class ItemId(Enum):
    NONE = 0
    SHORT_SWORD = 2
    WAND_1 = 3
    FOOD_RATION = 4
    SKULL_KEY = 8
    KEY = 9
    GOLDEN_KEY = 10
    GOLD = 14
    SHURIKEN = 15
    KNUCKLEDUSTER = 16
    QUARTERSTAFF = 17
    MACE = 18
    DAGGER = 19
    SWORD = 20
    LONGSWORD = 21
    BATTLE_AXE = 22
    WAR_HAMMER = 23
    CLOTH_ARMOR = 24
    LEATHER_ARMOR = 25
    MAIL_ARMOR = 26
    SCALE_ARMOR = 27
    PLATE_ARMOR = 28
    SPEAR = 29
    GLAIVE = 30
    DART = 31
    RING_1 = 32
    RING_2 = 33
    RING_3 = 34
    RING_4 = 35
    RING_5 = 36
    RING_6 = 37
    RING_7 = 38
    RING_8 = 39
    SCROLL_1 = 40
    SCROLL_2 = 41
    SCROLL_3 = 42
    SCROLL_4 = 43
    SCROLL_5 = 44
    SCROLL_6 = 45
    SCROLL_7 = 46
    SCROLL_8 = 47
    WAND_2 = 48
    WAND_3 = 49
    WAND_4 = 50
    WAND_5 = 51
    WAND_6 = 52
    WAND_7 = 53
    WAND_8 = 54
    WAND_9 = 55
    POTION_1 = 56
    POTION_2 = 57
    POTION_3 = 58
    POTION_4 = 59
    POTION_5 = 60
    POTION_6 = 61
    POTION_7 = 62
    POTION_8 = 63
    POTION_9 = 64
    POTION_10 = 65
    POTION_11 = 66
    POTION_12 = 67
    WAND_10 = 68
    WAND_11 = 69
    WAND_12 = 70
    WAND_13 = 71
    RING_9 = 72
    RING_10 = 73
    RING_11 = 74
    RING_12 = 75
    SCROLL_9 = 76
    SCROLL_10 = 77
    SCROLL_11 = 78
    SCROLL_12 = 79
    UNKNOWN_1 = 80
    DEWDROP = 81
    UP_BOOK = 82
    SEED_POUCH = 83
    TORCH = 84
    RECALLER = 85
    ARMOR_KIT = 86
    AMULET_OF_YENDOR = 87
    FIRE_SEED = 88
    ICE_SEED = 89
    POISON_SEED = 90
    CONFUSION_SEED = 91
    HEALING_SEED = 92
    EARTH_SEED = 93
    UNK_SEED1 = 94
    UNK_SEED2 = 95
    UNKNOWN_ARMOR_1 = 96
    UNKNOWN_ARMOR_2 = 97
    UNKNOWN_ARMOR_3 = 98
    UNKNOWN_ARMOR_4 = 99
    ROSE = 100
    PICKAXE = 101
    GOLD_ORE = 102
    RAT_SKULL = 103
    SCROLL_HOLDER = 104
    CHEST_1 = 105
    BOOMERANG = 106
    HATCHET = 107
    FIRE_DART = 108
    PARALYZE_DART = 109
    JAVELIN = 110
    WAND_HOLDER = 111
    PASTY = 112
    RAW_MEAT = 113
    GRILLED_MEAT = 114
    OVERPRICED_RATION = 115
    FROZEN_MEAT = 116
    SCROLL_WIPE = 117
    UNKNOWN_2 = 118
    UNKNOWN_3 = 119
    DEW_VIAL = 120
    UNKNOWN_4 = 121
    WATER_4 = 122
    COUNTERWEIGHT = 123
    BOMB = 124
    HONEYPOT = 125
    KEYRING = 126
    UNKNOWN_6 = 127


dictItemTypes = {
    0: "none",
    2: "weapon",
    3: "weapon",
    4: "food",
    8: "key",
    9: "key",
    10: "key",
    14: "valuable",
    15: "ammo",
    16: "weapon",
    17: "weapon",
    18: "weapon",
    19: "weapon",
    20: "weapon",
    21: "weapon",
    22: "weapon",
    23: "weapon",
    24: "armor",
    25: "armor",
    26: "armor",
    27: "armor",
    28: "armor",
    29: "weapon",
    30: "weapon",
    31: "ammo",
    32: "accessory",
    33: "accessory",
    34: "accessory",
    35: "accessory",
    36: "accessory",
    37: "accessory",
    38: "accessory",
    39: "accessory",
    40: "scroll",
    41: "scroll",
    42: "scroll",
    43: "scroll",
    44: "scroll",
    45: "scroll",
    46: "scroll",
    47: "scroll",
    48: "wand",
    49: "wand",
    50: "wand",
    51: "wand",
    52: "wand",
    53: "wand",
    54: "wand",
    55: "wand",
    56: "potion",
    57: "potion",
    58: "potion",
    59: "potion",
    60: "potion",
    61: "potion",
    62: "potion",
    63: "potion",
    64: "potion",
    65: "potion",
    66: "potion",
    67: "potion",
    68: "wand",
    69: "wand",
    70: "wand",
    71: "wand",
    72: "ring",
    73: "ring",
    74: "ring",
    75: "ring",
    76: "scroll",
    77: "scroll",
    78: "scroll",
    79: "scroll",
    80: "unknown",
    81: "other",
    82: "other",
    83: "container",
    84: "other",
    85: "other",
    86: "other",
    87: "yendor",
    88: "seed",
    89: "seed",
    90: "seed",
    91: "seed",
    92: "seed",
    93: "seed",
    94: "seed",
    95: "seed",
    96: "armor",
    97: "armor",
    98: "armor",
    99: "armor",
    100: "other",
    101: "other",
    102: "other",
    103: "other",
    104: "container",
    105: "other",
    106: "ammo",
    107: "ammo",
    108: "ammo",
    109: "ammo",
    110: "ammo",
    111: "container",
    112: "food",
    113: "food",
    114: "food",
    115: "food",
    116: "food",
    117: "scroll",
    118: "other",
    119: "other",
    120: "container",
    121: "other",
    122: "other",
    123: "other",
    124: "ammo",
    125: "other",
    126: "container",
    127: "other",
}

def statusPersonagem():

    process = rwm.get_process_by_name("PD.exe")
    process.open()
    baseAddress_HP = pymem.process.module_from_name(pm.process_handle, "jvm.dll").lpBaseOfDll

    stats_HitPoints = process.read(process.get_pointer(baseAddress_HP + 0x0036E654, offsets=[0x40, 0x464, 0x38, 0x58, 0x18]))
    #print(stats_HitPoints)
    return stats_HitPoints
#statusPersonagem()