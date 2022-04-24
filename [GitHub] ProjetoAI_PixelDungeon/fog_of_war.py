import numpy as np
import sys
#from PIL import Image as im
from ReadWriteMemory import ReadWriteMemory
import pymem
from utils import *
from enum import Enum, unique
import time
start_time = time.time()
pm = pymem.Pymem("PD.exe")
rwm = ReadWriteMemory()

# 24/10/2021
# Henrique Serveira dos Santos

process = rwm.get_process_by_name("PD.exe")
process.open()

baseAddress_fog_of_war = pymem.process.module_from_name(pm.process_handle, "jvm.dll").lpBaseOfDll

#31x31?= 961
def read_fog_of_war():

    pointerteste = 0x110 #offset inicial
    fogOfwar = []
    for pointerteste in range(pointerteste, pointerteste + 0x1f78, 0x100):  #precisa iterar do offset inicial até
        # a últ. linha, pulando uma linha #0x1e78
        for pointerteste in range(pointerteste, pointerteste + 0x80, 0x4):  #offset entre pontos é 0x4, o offset real vai só até 0x7c,
            # mas aí gera uma matrix 31x31. como o valor após 0x7c é 4278190080, _
            #acc_offset = 0x108 + pointer_num * 0x4                         #deixei assim pra facilitar na hora de converter pro minimapa
            pointer = process.read(process.get_pointer(baseAddress_fog_of_war + 0x0036E5E4, offsets=[0x38, 0x70, 0xd8, 0x74, 0x30, 0x84, pointerteste]))
            #print(hex(pointer), pointer)
            #print(hex(process.get_pointer(baseAddress_fog_of_war + 0x0036E5E4, offsets=[0x38, 0x70, 0xd8, 0x74, 0x30, 0x84, pointerteste])))

            # 0xff000000 4278190080 #invisible # 2
            # 0xcc111111 3423670545 # visited # 1
            # 0x0 0 # visible # 0

            #codificação one-hot [0: visible | 3423670545: visited | 4278190080: invisible]
            if pointer == 0: # visible
                fogOfwar.append(pointer)
            elif pointer == 3423670545: #visited
                fogOfwar.append(1)
            elif pointer == 4278190080: #invisible
                fogOfwar.append(2)

    fogOfWar = np.array(fogOfwar) #\/ ajustes pra entrar no tensor
    fogOfWar.reshape(32, 32)
    fogOfWar = fogOfWar.astype(np.float32)
    return fogOfwar
#fogOfWar = read_fog_of_war()