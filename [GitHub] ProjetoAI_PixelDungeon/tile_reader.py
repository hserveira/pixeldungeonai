import numpy as np
import sys
from ReadWriteMemory import ReadWriteMemory
import pymem
import torch
from utils import *
from enum import Enum, unique
import time
start_time = time.time()
pm = pymem.Pymem("PD.exe")
rwm = ReadWriteMemory()

# 04/10/2021 - início do projeto (pesquisa)
# 13/10/2021 - início do desenvolvimento do código
# 01/11/2021 - ok

process = rwm.get_process_by_name("PD.exe")
process.open()

baseAddress_porta = pymem.process.module_from_name(pm.process_handle, "jvm.dll").lpBaseOfDll


#O mapa do jogo é um grid 32x32 que inicia no endereço com offset 0xC e vai até 0x1000
def read_tiles():
    #dungeonDepth = process.read(process.get_pointer(baseAddress_porta + 0x0036E5E4, offsets=[0x800, 0x40, 0x4C4, 0x38, 0xE0]))
    tiles = []
    for pointer_num in range(2, 1026):
        dungeonDepth = process.read(
            process.get_pointer(baseAddress_porta + 0x0036E5E4, offsets=[0x800, 0x40, 0x4C4, 0x38, 0xE0]))
        acc_offset = 0x4 * pointer_num + 0x4
        pointer = process.read(process.get_pointer(baseAddress_porta + 0x0036D620, offsets=[0x58, 0x40, 0x464, 0x38, 0x5c, 0x1c, acc_offset]))
        #print(mapa)
        #print(pointer)
        tiles.append(pointer)

    tiles = np.array(tiles) #\/ ajustes pra entrar no tensor
    tiles.reshape(32, 32)
    #print(tiles.reshape(32, 32))
    tiles = tiles.astype(np.float32)

    return tiles
#tiles = read_tiles()

def read_depth():
    dungeonDepth = process.read(process.get_pointer(baseAddress_porta + 0x0036E5E4, offsets=[0x800, 0x40, 0x4C4, 0x38, 0xE0]))
    #print(dungeonDepth)
    return dungeonDepth
#read_depth()
